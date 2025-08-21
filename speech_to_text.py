import queue
import time
import webrtcvad
import sounddevice as sd
import tempfile
import os
from config import SAMPLE_RATE, BLOCK_MS, VAD_AGGRESSIVENESS, SILENCE_AFTER_SPEECH_S
from audio_utils import save_wav
import whisper

def load_whisper_model(model_name: str):
    """Load the Whisper model."""
    print("🔄 Loading Whisper model...")
    try:
        return whisper.load_model(model_name)
    except Exception as e:
        print(f"❌ Failed to load Whisper model: {e}")
        raise

def listen_forever(whisper_model, on_speech_detected):
    """Listen continuously for speech and transcribe using Whisper."""
    vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)
    block_frames = int(SAMPLE_RATE * (BLOCK_MS / 1000.0))  # e.g., 480 for 30 ms @ 16 kHz
    q = queue.Queue()
    frames = []
    last_voice_time = None
    speaking = False

    def callback(indata, frames_count, time_info, status):
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))

    print("🎙 Listening continuously. Speak to me... (say 'stop' to exit)")
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=block_frames,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        while True:
            try:
                frame = q.get()
                is_speech = vad.is_speech(frame, SAMPLE_RATE)

                if is_speech:
                    print("🎤 Speech detected...", end="\r")
                    frames.append(frame)
                    last_voice_time = time.time()
                    speaking = True
                elif speaking:
                    if last_voice_time and (time.time() - last_voice_time > SILENCE_AFTER_SPEECH_S):
                        audio_bytes = b"".join(frames)
                        frames.clear()
                        speaking = False
                        last_voice_time = None

                        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpf:
                            wav_path = tmpf.name
                        save_wav(wav_path, audio_bytes, SAMPLE_RATE)

                        print("\n🔍 Transcribing...")
                        try:
                            text = whisper_model.transcribe(wav_path)["text"].strip()
                        except Exception as e:
                            print(f"❌ Whisper error: {e}")
                            text = ""
                        finally:
                            try:
                                os.remove(wav_path)
                            except Exception:
                                pass

                        if text:
                            print(f"📝 You said: {text}")
                            on_speech_detected(text)

            except KeyboardInterrupt:
                print("\n👋 Exiting. Goodbye!")
                return
            except Exception as e:
                print(f"❌ Listening error: {e}")
                frames.clear()
                speaking = False
                last_voice_time = None
import wave
import numpy as np
import sounddevice as sd
from config import SAMPLE_RATE

def save_wav(filename: str, audio_bytes: bytes, sample_rate: int = SAMPLE_RATE):
    """Save audio bytes to a WAV file."""
    try:
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_bytes)
    except Exception as e:
        print(f"❌ WAV save error: {e}")

def play_wav_file(path: str):
    """Play a WAV file using sounddevice."""
    try:
        with wave.open(path, "rb") as wav_file:
            sr = wav_file.getframerate()
            frames = wav_file.readframes(wav_file.getnframes())
            audio = np.frombuffer(frames, dtype=np.int16)
        sd.play(audio, samplerate=sr)
        sd.wait()
    except Exception as e:
        print(f"❌ Playback error: {e}")
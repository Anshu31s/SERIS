import tempfile
import wave
import os
import re
from piper import PiperVoice, SynthesisConfig
from audio_utils import play_wav_file

def _detect_cuda_for_piper() -> bool:
    """Detect if CUDA is available for Piper."""
    try:
        test_voice = PiperVoice.load("voices/en_US-amy-medium.onnx", use_cuda=True)
        del test_voice
        return True
    except Exception:
        return False

def load_piper_voice(model_path: str):
    """Load the Piper voice model."""
    use_cuda = _detect_cuda_for_piper()
    try:
        piper_voice = PiperVoice.load(model_path, use_cuda=use_cuda)
        print(f"🗣 Piper voice loaded ({'GPU' if use_cuda else 'CPU'})")
        return piper_voice, use_cuda
    except Exception as e:
        print(f"❌ Failed to load Piper voice model: {e}")
        raise

def clean_text_for_tts(text: str) -> str:
    """Remove emojis and basic markdown for cleaner TTS."""
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub(r'', text)
    text = re.sub(r'(\*\*|\*|_|\#|\[|\]|\(|\))', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def speak_text(text: str, piper_voice, synthesis_config):
    """Synthesize and play text using Piper TTS."""
    if not text.strip():
        return
    cleaned_text = clean_text_for_tts(text)
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        with wave.open(tmp_path, "wb") as wf:
            piper_voice.synthesize_wav(cleaned_text, wf, syn_config=synthesis_config)
        play_wav_file(tmp_path)
    except Exception as e:
        print(f"❌ Piper TTS error: {e}")
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass
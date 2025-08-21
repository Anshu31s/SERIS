import os

# Audio settings
SAMPLE_RATE = 16000
BLOCK_MS = 30  # Valid for webrtcvad: 10/20/30
SILENCE_AFTER_SPEECH_S = 5.0
VAD_AGGRESSIVENESS = 2  # 0-3

# Model settings
ASR_MODEL = os.getenv("WHISPER_MODEL", "base")  # tiny/base/small/medium/large
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:latest")
SPEAK_STREAMING = True  # Speak sentence-by-sentence as LLM streams

# Piper TTS settings
PIPER_VOICE_MODEL = "voices/en_US-amy-medium.onnx"
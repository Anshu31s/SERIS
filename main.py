import sys
import time
import ollama
from config import ASR_MODEL, OLLAMA_MODEL, SPEAK_STREAMING, PIPER_VOICE_MODEL
from speech_to_text import load_whisper_model, listen_forever
from text_to_speech import load_piper_voice, speak_text, SynthesisConfig

def warmup_ollama():
    """Warm up the Ollama model."""
    print("🔄 Warming up Ollama model...")
    try:
        t0 = time.time()
        ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Respond in plain text without emojis or markdown."},
                {"role": "user", "content": "Hello"}
            ]
        )
        print(f"✅ Ollama warmed up in {time.time() - t0:.2f} seconds")
    except Exception as e:
        print(f"❌ Ollama warm-up error: {e}")

def _sentences_from_stream(chunks_iter):
    """Yield sentences as they complete (ends with ., !, ?, or newline)."""
    buffer = ""
    enders = (".", "!", "?", "\n")
    for chunk in chunks_iter:
        content = chunk["message"]["content"]
        buffer += content
        print(content, end="", flush=True)
        while True:
            idxs = [buffer.find(e) for e in enders if buffer.find(e) != -1]
            if not idxs:
                break
            cut = min(idxs) + 1
            sent, buffer = buffer[:cut], buffer[cut:]
            yield sent
    if buffer.strip():
        yield buffer

def query_ollama(input_text: str, piper_voice, synthesis_config):
    """Query Ollama and optionally stream TTS."""
    try:
        full = []
        if SPEAK_STREAMING:
            print("🤖 Ollama says: ", end="", flush=True)
            stream = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant. Respond in plain text without emojis or markdown."},
                    {"role": "user", "content": input_text}
                ],
                stream=True
            )
            for sentence in _sentences_from_stream(stream):
                full.append(sentence)
                speak_text(sentence, piper_voice, synthesis_config)
            print()
            return "".join(full).strip()
        else:
            print("🤖 Ollama says: ", end="", flush=True)
            for chunk in ollama.chat(
                model=OLLAMA_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant. Respond in plain text without emojis or markdown."},
                    {"role": "user", "content": input_text}
                ],
                stream=True
            ):
                content = chunk["message"]["content"]
                full.append(content)
                print(content, end="", flush=True)
            print()
            response = "".join(full).strip()
            if response:
                speak_text(response, piper_voice, synthesis_config)
            return response
    except Exception as e:
        print(f"\n❌ Ollama error: {e}")
        return ""

def main():
    """Main application loop."""
    # Initialize models
    whisper_model = load_whisper_model(ASR_MODEL)
    piper_voice, use_cuda = load_piper_voice(PIPER_VOICE_MODEL)
    synthesis_config = SynthesisConfig(
        volume=0.7,
        length_scale=1.0,
        noise_scale=1.0,
        noise_w_scale=1.0,
        normalize_audio=True
    )
    warmup_ollama()

    # Define callback for speech detection
    def on_speech_detected(text):
        if text.lower() in {"stop", "exit", "quit"}:
            print("👋 Goodbye!")
            sys.exit(0)
        response = query_ollama(text, piper_voice, synthesis_config)
        if response and not SPEAK_STREAMING:
            speak_text(response, piper_voice, synthesis_config)

    # Start listening
    try:
        listen_forever(whisper_model, on_speech_detected)
    except KeyboardInterrupt:
        print("\n👋 Exiting. Goodbye!")
    except Exception as e:
        print(f"❌ Main error: {e}")

if __name__ == "__main__":
    main()
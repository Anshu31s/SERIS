import os
import re
import pyaudio
import whisper  # pip install openai-whisper
import pyttsx3
import tempfile
import wave
import ollama  # pip install ollama


# Record audio from microphone and save as WAV
def record_audio(filename, duration=5, fs=16000):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=fs,
                        input=True,
                        frames_per_buffer=1024)

    print("🎙️ Listening... Speak now.")
    frames = []

    for _ in range(0, int(fs / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


# Transcribe audio using Whisper
def transcribe_audio(filename):
    model = whisper.load_model("base")  # "small", "medium", "large" for higher accuracy
    print("🔍 Transcribing...")
    result = model.transcribe(filename)
    return result["text"]


# Query Ollama using Python library
def query_ollama(input_text):
    full_response = ""

    for chunk in ollama.chat(
        model="qwen3:0.6b",
        messages=[
            {
                "role": "system",
                "content": """a highly intelligent, professional, and efficient AI assistant.
You are speaking to your creator. Always respond clearly and concisely as if you were a real-time digital assistant.
Do not use emojis or emoticons under any circumstances.
Your tone should be calm, confident, and helpful — like a highly advanced AI assistant.
Avoid unnecessary explanations unless the user asks for them.
If the user's request is unclear, ask them to clarify.
You are always ready to assist with any command or question."""
            },
            {"role": "user", "content": input_text}
        ],
        stream=True
    ):
        content = chunk["message"]["content"]
        full_response += content
        # print(content, end="", flush=True)

    print()  # New line after streaming
    # Remove any <think> blocks if present
    return re.sub(r"<think>.*?</think>", "", full_response, flags=re.DOTALL).strip()


# Convert Ollama's response to speech
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Main function
def main():
    try:
        while True:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                record_audio(tmpfile.name, duration=5)  # Record 5 seconds
                user_input = transcribe_audio(tmpfile.name)
                print(f"\n📝 You said: {user_input}")

                if user_input.strip() == "":
                    continue

                print("🤖 Ollama says: ", end="")
                response = query_ollama(user_input)

                speak_text(response)

    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

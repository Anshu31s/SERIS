# SERIS

**Self-Evolving Responsive Intelligence System**

SERIS is a work-in-progress **offline AI assistant** that listens, thinks, and responds naturally.
It combines **speech recognition (Whisper)**, **local reasoning (Ollama)**, and **speech synthesis (Piper TTS)** to create a real-time interactive assistant — all running on your own machine.

---

## ✨ Features

* 🎙️ **Voice Input** – Detects speech using `webrtcvad`.
* 📝 **Speech-to-Text (STT)** – Converts your voice to text with `Whisper`.
* 🧠 **Offline Reasoning** – Uses `Ollama` (local LLMs) to generate intelligent responses.
* 🔊 **Text-to-Speech (TTS)** – Responds back using natural speech via `Piper TTS`.
* ⚡ **Real-Time Interaction** – Powered by `sounddevice` for low-latency audio input/output.
* 🔒 **Runs 100% Locally** – No cloud required. Your data stays on your computer.

---

## 🛠️ Tech Stack

* **[Ollama](https://ollama.ai/)** → Local LLMs (offline chat & reasoning)
* **[Whisper](https://github.com/openai/whisper)** → Speech-to-text transcription
* **[Piper TTS](https://github.com/OHF-Voice/piper1-gpl)** → Natural text-to-speech
* **[sounddevice](https://python-sounddevice.readthedocs.io/)** → Real-time audio I/O
* **[webrtcvad](https://github.com/wiseman/py-webrtcvad)** → Voice activity detection

---

## 🚀 Getting Started
### 1. Install Ollama

Download and install Ollama from: [https://ollama.ai](https://ollama.ai)

Verify it’s running:

```bash
ollama run llama3
```

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/seris.git
cd seris
```

### 3. Install PyTorch (GPU recommended)

Make sure to install PyTorch with CUDA (for Whisper & Piper TTS):

```bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu129
```

*(If you don’t have an NVIDIA GPU, install the CPU version from [PyTorch.org](https://pytorch.org/get-started/locally/)).*

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run SERIS

```bash
python main.py
```

---

## 📌 Roadmap

* [x] Offline speech-to-text with Whisper
* [x] Offline reasoning with Ollama
* [x] Offline text-to-speech with Piper
* [ ] Add memory (short & long term)
* [ ] Build a GUI
* [ ] Add system/app control (open apps, read files, automation)
* [ ] IoT integrations (smart devices)

---

## 📜 License

MIT License © 2025

---

⚡ **SERIS — A truly local AI assistant. No cloud. No leaks. 100% yours.**
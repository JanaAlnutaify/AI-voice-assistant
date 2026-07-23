# 🎙️ AI Voice Assistant with Cohere & Whisper

An intelligent Arabic voice assistant that combines **Whisper** for speech recognition, **Cohere AI** for natural language understanding, and **gTTS** for generating spoken responses.

---

## ✨ Key Features

* 🎙️ **Speech-to-Text:** Converts spoken Arabic into text using Whisper and SpeechRecognition.
* 🧠 **AI-Powered Responses:** Generates intelligent responses using Cohere AI.
* 🔊 **Text-to-Speech:** Converts AI responses into Arabic speech using gTTS.
* 🖥️ **Modern GUI:** Interactive user interface built with CustomTkinter.
* 🌐 **Arabic Language Support:** Designed to process and respond naturally in Arabic.

---

## 🛠️ Technologies Used

* **Python**
* **Whisper** – Speech Recognition
* **Cohere AI** – Natural Language Processing
* **gTTS** – Text-to-Speech
* **SpeechRecognition** – Audio Input Processing
* **CustomTkinter** – Graphical User Interface
* **Pygame** – Audio Playback
* **Arabic Reshaper** – Arabic Text Processing

---

## 📸 Interface & Preview

### 1️⃣ Main Application Interface

![Main Interface](intarface.png)

### 2️⃣ Interaction & Question Sample

![Application Prompt](pic1.png)

---

## 🎥 Video Demo

Watch the AI voice assistant in action:

[![Watch the demo](https://youtube.com/shorts/4C_h__ag-Hw?feature=share/maxresdefault.jpg)](https://youtube.com/shorts/4C_h__ag-Hw?feature=share)


## 🔑 Prerequisites & API Key Setup

Before running the application, you need to obtain a **Cohere API Key**.

🔗 **Get your API Key:** [Cohere API Keys](https://dashboard.cohere.com/api-keys)

> ⚠️ **Important:** COHERE_API_KEY=********** replace with your API key

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/JanaAlnutaify/YOUR-REPOSITORY-NAME.git
cd YOUR-REPOSITORY-NAME
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
python voiceToText.py
```

---

## 📁 Repository Structure

| File Name          | Description                                                                       |
| :----------------- | :-------------------------------------------------------------------------------- |
| `voiceToText.py`   | Main application script handling GUI, audio input, AI processing, and TTS output. |
| `requirements.txt` | List of required Python packages and dependencies.                                |
| `intarface.png`    | Screenshot of the main interface layout.                                          |
| `pic1.png`         | Screenshot showcasing an interactive Q&A session.                                 |
| `README.md`        | Project documentation.                                                            |

---

## 📌 Notes

* An active internet connection is required for Cohere AI and gTTS services.
* A working microphone is required for voice input.
* The Cohere API Key must be configured before running the application.

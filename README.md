# Voice-to-FIR Generator

A system that automates **First Information Report (FIR) generation** from voice recordings using AI. This project integrates **Whisper AI** for speech-to-text conversion and **Gemini AI** for FIR generation. It also includes a **case status search API** and **fine-tuned Qwen models** with **RAG** implementation for Indian law-based queries.

---

## Features

- 🎙 **Audio-to-Text**: Converts victim's voice recordings to text using **Whisper AI**.
- 📜 **FIR Generation**: Uses **Gemini AI** to generate structured FIR documents.
- 🔍 **Case Status Search API**: Allows searching case details using **Case ID**.
- 🤖 **Fine-tuned Qwen (0.5 - 1.5) Models**: Trained on **Indian legal datasets** for better FIR accuracy.
- 📚 **RAG (Retrieval-Augmented Generation)**: Enhances model responses with **legal knowledge retrieval**.

---

## Structure
- **Main Branch (main):** Contains Whisper AI and Gemini AI FIR generation.
- **Fine-Tuning Repo:** [https://github.com/ajf1016/Fine-Tuning-Qwen1.5-0.5B]
  [https://github.com/ajf1016/Fine-Tuning-Qwen1.5-0.5B]
- **RAG Implementation Repo:** [https://github.com/ajf1016/Qwen-RAG-for-legal-queries]

## Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/ajf1016/AI-Voice-to-FIR-Converter-.git
   cd voice-to-fir
   ```

2. **Set Up the Virtual Environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
   
4. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```
6. **Set Up Environment Variables Create a .env file and add:**
   ```
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```
7. **Run the Django Server**
   ```
   python manage.py runserver
   ```
## API Endpoints
1️⃣ Upload & Convert Audio[aznet@archlinux AI-Voice-to-FIR-Converter-]$ psql -U root -p
psql: option requires an argument -- 'p'
psql: hint: Try "psql --help" for more information.
[aznet@archlinux AI-Voice-to-FIR-Converter-]$ 
Endpoint: POST /api/upload/
Description: Uploads an audio file and converts it into text using Whisper AI.

Request Example (form-data):
```
audio_file: <file.mp3>
```

2️⃣ Generate FIR
Endpoint: POST /api/fir/<id>/
Description: Generates an FIR using Gemini AI from transcribed text.

Headers:
```
Authorization: Bearer <token>
```

3️⃣ Search Case Status
Endpoint: GET /api/fir/CASE-<case_id>/
Description: Retrieves FIR details using a Case ID.

4️⃣ User Registration
Endpoint: POST /api/register/
Request Body (JSON):
```
{
  "full_name": "Test User",
  "uid": "123456",
  "phone": "0000000000",
  "password": "securepassword"
}
```

5️⃣ User Login
Endpoint: POST /api/login/
Request Body (JSON):
```
{
  "uid": "123456",
  "password": "securepassword"
}
```

## Acknowledgment
This project utilizes datasets from another GitHub repository for model training. Special thanks to the original dataset creator. 🎖 https://github.com/civictech-India/Indian-Law-Penal-Code-Json/tree/main

## Contributing
Contributions are welcome! Feel free to open an issue or pull request.
For major changes, please discuss them in advance.








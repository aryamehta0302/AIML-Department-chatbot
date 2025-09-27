# 🤖 AIML Department Chatbot Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-black?logo=flask)](https://flask.palletsprojects.com/)
[![Google Gemini](https://img.shields.io/badge/Gemini-API-blueviolet?logo=google)](https://ai.google.dev/)
[![TF-IDF](https://img.shields.io/badge/TF--IDF-Retrieval-green)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

> 🎓 Smart departmental assistant for the **AI & Machine Learning Department**, built using **Flask**, **Google Gemini API**, and **TF-IDF retrieval**.

---

## 🎬 Demo

🎥 **Watch the full working demo:**  
[Demo Video](assets/demo.mp4)


---

## ✨ Features

✅ **AI-Powered Responses** — Uses **Google Gemini Flash** model  
✅ **TF-IDF Context Retrieval** — Retrieves relevant knowledge base data  
✅ **Multilingual Support** — English, Hindi, Gujarati, Tamil, Telugu  
✅ **Voice Input & Output** — Speak your query, get audio responses  
✅ **Follow-up Memory** — Remembers last 2 questions for context  
✅ **Clean UI** — Built with Bootstrap 5  
✅ **Guardrails** — Blocks unsafe queries  
✅ **Quick Links + FAQ Section** — Navigation-friendly design

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Backend** | Flask (Python) |
| **AI Model** | Google Gemini (Flash) |
| **Search** | TF-IDF + Cosine Similarity |
| **Translation** | `deep-translator` |
| **Voice** | Web Speech API |

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd AIML-Department-chatbot
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate     # On Windows
# OR
source venv/bin/activate    # On Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your environment variable
Create a `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

### 5. Build your TF-IDF index
```bash
python build_index.py
```

### 6. Run the app
```bash
python app.py
```
Go to 👉 **http://127.0.0.1:5000/**

---

## 🌍 Supported Languages

| Language | Code |
|----------|------|
| English  | `en` |
| Hindi    | `hi` |
| Gujarati | `gu` |
| Tamil    | `ta` |
| Telugu   | `te` |

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

⭐ **Star this project** if you like it!

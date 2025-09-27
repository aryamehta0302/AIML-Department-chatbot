
# 🎓 AI-Enabled Intelligent Assistant for Departmental Query Management

An interactive chatbot system built for the **AIML Department at CSPIT, CHARUSAT** to handle queries about admissions, faculty, courses, research, and more.  
This assistant combines **local document indexing (TF-IDF)** with **Gemini AI** to provide professional, safe, and structured responses.

---

## ✨ Features
- 🗂️ **Knowledge Base Search**: Answers based on department data (faculty, courses, admissions, etc.).  
- 🧠 **Gemini Integration**: Polished, natural, and professional responses.  
- 🔒 **Guardrails**: Blocks unsafe/off-topic queries (violence, NSFW, etc.).  
- 🎨 **UI/UX Improvements**: Modern responsive interface with Bootstrap.  
- 📝 **Smart Formatting**: Replies use bullet points, bold text, and tables where needed.  
- ⚡ **Lightweight & Free**: Uses TF-IDF for retrieval (no embedding quota issues).  

---

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS (Bootstrap), JavaScript  
- **Backend:** Python (Flask)  
- **AI Model:** Google Gemini (gemini-1.5-flash)  
- **Retrieval:** TF-IDF (Scikit-learn)  
- **Vector Storage (legacy):** FAISS (optional)  

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/aiml-department-assistant.git
cd aiml-department-assistant
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_api_key_here
```

### 5. Build the TF-IDF index
```bash
python build_index.py
```

### 6. Run the server
```bash
python app.py
```
Visit 👉 `http://127.0.0.1:5000`

---

## 📂 Project Structure
```
├── app.py              # Flask backend with chatbot logic
├── build_index.py      # Builds TF-IDF index from /data files
├── data/               # Department data in .txt format
├── templates/          # HTML pages (index, faculty, admissions, etc.)
├── static/             # CSS, JS, images
├── faiss_index/        # Stores docs.pkl, vectorizer.pkl, vectors.npy
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 📸 Screenshots (placeholders)
![Chatbot Screenshot](static/images/demo.png)  
*Interactive chatbot UI for AIML Department queries*

---

## 📊 Future Enhancements
- Hybrid retrieval (TF-IDF + embeddings) for better accuracy.  
- Integration of structured data (JSON/CSV for faculty/courses).  
- Improved multilingual support.  
- Deployment on Vercel/Render/Heroku.  

---

## 🏆 Credits
Developed by **Arya Mehta (23AIML036)** under guidance of faculty, AIML Department, CSPIT CHARUSAT.

---

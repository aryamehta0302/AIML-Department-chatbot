import os
import pickle
import re
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from langchain_google_genai import ChatGoogleGenerativeAI
from deep_translator import GoogleTranslator  # ✅ Translation

# ================== Load API Key ==================
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise RuntimeError("❌ Please set GEMINI_API_KEY in your .env file")

# ================== Flask App ==================
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

INDEX_DIR = "./faiss_index"

# ================== Load TF-IDF Index ==================
with open(os.path.join(INDEX_DIR, "docs.pkl"), "rb") as f:
    documents = pickle.load(f)
with open(os.path.join(INDEX_DIR, "vectorizer.pkl"), "rb") as f:
    vectorizer = pickle.load(f)
vectors = np.load(os.path.join(INDEX_DIR, "vectors.npy"))

# ================== Gemini Model ==================
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=GEMINI_KEY
)

# ================== Memory ==================
memory = []  # store last 2-3 messages as [(q, a), ...]

# ================== Helpers ==================
def clean_answer(text: str) -> str:
    """Clean repetitive prefixes from Gemini replies."""
    if not text:
        return text
    patterns = [
        r"^based on (the )?provided text[:,]?\s*",
        r"^according to (the )?(context|text)[:,]?\s*",
        r"^from (the )?(given|provided) (text|information)[:,]?\s*",
        r"^as mentioned (in|by) (the )?text[:,]?\s*",
        r"^the passage (states|suggests)[:,]?\s*",
        r"^in (summary|conclusion)[:,]?\s*",
        r"^to (summarize|conclude)[:,]?\s*"
    ]
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text.strip()


def retrieve_docs(query, k=5):
    """Retrieve top-k docs using TF-IDF cosine similarity."""
    q_vec = vectorizer.transform([query]).toarray()
    sims = cosine_similarity(q_vec, vectors)[0]
    top_idx = sims.argsort()[-k:][::-1]
    return [documents[i] for i in top_idx if sims[i] > 0.1]


def is_blocked(query: str) -> bool:
    blocked_keywords = [
        "politics", "religion", "terrorism", "violence",
        "sex", "porn", "murder", "bomb", "drugs", "suicide"
    ]
    return any(word in query.lower() for word in blocked_keywords)


# ================== Routes ==================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admissions")
def admissions():
    return render_template("admissions.html")

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/faculty")
def faculty():
    return render_template("faculty.html")

@app.route("/research")
def research():
    return render_template("research.html")

@app.route("/ask", methods=["POST"])
def ask_endpoint():
    global memory
    body = request.get_json(force=True)
    question = (body.get("question", "") or "").strip()
    language = body.get("language", "en")  # default English

    if not question:
        return jsonify({"error": "❌ question required"}), 400

    # 🚫 Guardrail
    if is_blocked(question):
        msg = "⚠️ Sorry, I cannot answer this question."
        translated = (
            GoogleTranslator(source="auto", target=language).translate(msg)
            if language != "en" else msg
        )
        return jsonify({"question": question, "answer": translated})

    try:
        # 📚 Retrieve related docs
        docs = retrieve_docs(question, k=5)
        context = "\n\n".join([d.page_content for d in docs]) if docs else ""

        # 🧠 Include last 2 turns for short-term memory
        memory_context = ""
        if memory:
            last_two = memory[-2:]
            memory_context = "\n\n".join([f"User: {q}\nAssistant: {a}" for q, a in last_two])

        # 🧾 Build prompt
        prompt = f"""
You are the AIML Department Assistant at CHARUSAT.
You must use context and memory to give accurate, continuous answers.

Past conversation:
{memory_context}

Knowledge Base Context:
{context}

User question: {question}

Guidelines:
- Be professional, friendly, concise.
- If user refers to 'him/her/they/that', use prior context to identify who/what they mean.
- Do NOT ask user to repeat if context is clear.
- Use bullet points if listing.
- Keep answers factual and polite.

Answer:
"""

        # 🤖 Generate answer
        response = llm.invoke(prompt)
        answer_en = clean_answer(
            response.content if hasattr(response, "content") else str(response)
        )

        # 💬 Save in memory (keep last 3 only)
        memory.append((question, answer_en))
        if len(memory) > 3:
            memory = memory[-3:]

        # 🌐 Translate if needed
        if language != "en":
            answer_final = GoogleTranslator(source="auto", target=language).translate(answer_en)
        else:
            answer_final = answer_en

        return jsonify({
            "question": question,
            "answer": answer_final
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================== Run ==================
if __name__ == "__main__":
    print("✅ AIML Assistant running at http://127.0.0.1:5000/")
    app.run(host="0.0.0.0", port=5000, debug=True)

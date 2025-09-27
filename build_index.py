# build_index.py (TF-IDF only, fixed)
import os
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

DATA_DIR = "./data"
INDEX_DIR = "./faiss_index"

def build_index():
    docs = []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".txt"):
            with open(os.path.join(DATA_DIR, fname), "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    docs.append(Document(page_content=content, metadata={"source": fname}))

    if not docs:
        docs = [Document(page_content="This is the AIML department knowledge base.",
                         metadata={"source": "builtin"})]

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    split_docs = splitter.split_documents(docs)

    texts = [doc.page_content for doc in split_docs]

    # Train TF-IDF
    vectorizer = TfidfVectorizer(max_features=1024)
    vectors = vectorizer.fit_transform(texts).toarray()

    # Save documents, vectorizer, and vectors
    os.makedirs(INDEX_DIR, exist_ok=True)
    with open(os.path.join(INDEX_DIR, "docs.pkl"), "wb") as f:
        pickle.dump(split_docs, f)
    with open(os.path.join(INDEX_DIR, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)
    np.save(os.path.join(INDEX_DIR, "vectors.npy"), vectors)

    print(f"✅ TF-IDF index built and saved at {INDEX_DIR}")

if __name__ == "__main__":
    build_index()

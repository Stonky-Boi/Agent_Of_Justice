import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.settings import GOOGLE_API_KEY

def load_legal_chunks(base_dir="legal_knowledge"):
    docs = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    text = f.read()
                    for chunk in splitter.split_text(text):
                        docs.append({"content": chunk, "source": os.path.join(root, file)})
    return docs

def build_legal_vectorstore():
    docs = load_legal_chunks()
    texts = [doc["content"] for doc in docs]
    metadatas = [{"source": doc["source"]} for doc in docs]
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    vs = FAISS.from_texts(texts, embedding=embeddings, metadatas=metadatas)
    vs.save_local("legal_vectorstore")
    print("Legal knowledge base vectorstore saved.")

def load_legal_vectorstore():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    return FAISS.load_local("legal_vectorstore", embeddings, allow_dangerous_deserialization=True)

def retrieve_legal(query, vectorstore, k=3):
    results = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([f"[Legal Reference from {r.metadata['source']}]:\n{r.page_content}" for r in results])

if __name__ == "__main__":
    build_legal_vectorstore()

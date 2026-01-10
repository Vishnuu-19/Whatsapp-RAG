import sys

def check(module_name, test_fn=None):
    try:
        module = __import__(module_name)
        if test_fn:
            test_fn(module)
        print(f"[OK] {module_name}")
    except Exception as e:
        print(f"[FAIL] {module_name} -> {e}")
        sys.exit(1)

# ---- Core Python libs ----
check("pandas")
check("numpy")
check("regex")
check("tqdm")
check("dateutil")

# ---- spaCy + model ----
def test_spacy(spacy):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp("Madhu discussed WTP yesterday")
    assert len(doc) > 0

check("spacy", test_spacy)

# ---- Embeddings ----
def test_embeddings(st):
    model = st.SentenceTransformer("all-MiniLM-L6-v2")
    vec = model.encode("What did Madhu say about WTP?")
    assert len(vec) == 384

check("sentence_transformers", test_embeddings)
check("torch")

# ---- Vector DB (Chroma) ----
def test_chroma(chromadb):
    client = chromadb.Client()
    col = client.create_collection("test_collection")
    col.add(
        documents=["Madhu discussed WTP model"],
        metadatas=[{"sender": "Madhu"}],
        ids=["1"]
    )
    res = col.query(query_texts=["WTP"], n_results=1)
    assert len(res["documents"][0]) > 0

check("chromadb", test_chroma)

# ---- LangChain ----
def test_langchain(langchain):
    from langchain.schema import Document
    d = Document(page_content="Madhu talked about WTP", metadata={"sender": "Madhu"})
    assert d.page_content

check("langchain")

# ---- Ollama (CLI check) ----
import subprocess

try:
    result = subprocess.run(
        ["ollama", "--version"],
        capture_output=True,
        text=True,
        check=True
    )
    print("[OK] ollama")
except Exception as e:
    print("[FAIL] ollama -> Ollama not found in PATH")
    sys.exit(1)

print("\n✅ ALL REQUIRED TOOLS ARE INSTALLED AND WORKING")

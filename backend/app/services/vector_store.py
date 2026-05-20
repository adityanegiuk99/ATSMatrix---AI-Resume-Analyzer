from functools import lru_cache
from chromadb import HttpClient
from app.core.config import settings


@lru_cache
def client():
    return HttpClient(host=settings.chroma_host, port=settings.chroma_port)


def upsert_resume(resume_id: str, text: str, metadata: dict) -> None:
    collection = client().get_or_create_collection("resume_knowledge")
    collection.upsert(ids=[resume_id], documents=[text], metadatas=[metadata])


def semantic_search(query: str, limit: int = 5) -> list[dict]:
    collection = client().get_or_create_collection("resume_knowledge")
    result = collection.query(query_texts=[query], n_results=limit)
    return [
        {"id": result["ids"][0][idx], "document": result["documents"][0][idx], "metadata": result["metadatas"][0][idx]}
        for idx in range(len(result.get("ids", [[]])[0]))
    ]

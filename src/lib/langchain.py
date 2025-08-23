from typing import List
from langchain_community.vectorstores import SQLiteVec
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import Settings

class LangChainClient:
    def __init__(self, db_file: str = Settings().db_file, table: str = "documents"):
        self.db_file = db_file
        self.table = table
        self.embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self._db = None

    def _ensure_db(self, texts: List[str]):
        self._db = SQLiteVec.from_texts(
            texts=texts,
            embedding=self.embedding,
            table=self.table,
            db_file=self.db_file,
        )

    def add_texts(self, texts: List[str]):
        if not texts:
            return
        if self._db is None:
            self._ensure_db(texts)
        else:
            self._db.add_texts(texts)

    def similarity_search(self, query: str, k: int = 4):
        if self._db is None:
            return []
        return self._db.similarity_search(query, k=k)

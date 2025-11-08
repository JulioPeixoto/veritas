from typing import List

from langchain_community.vectorstores import SQLiteVec
from langchain_openai import OpenAIEmbeddings

from src.config import settings


class LangChainClient:
    def __init__(self, db_file: str = settings.path_db_file, table: str = "documents"):
        self.db_file = db_file
        self.table = table
        self.embedding = OpenAIEmbeddings(
            model="text-embedding-3-small", api_key=settings.openai_api_key
        )
        self._db = None

    def init_db(self):
        try:
            self._db = SQLiteVec(
                table=self.table,
                embedding=self.embedding,
                db_file=self.db_file,
            )
        except Exception:
            self._db = SQLiteVec.from_texts(
                texts=[],
                embedding=self.embedding,
                table=self.table,
                db_file=self.db_file,
            )

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
            self.init_db()

        if self._db is None:
            return []

        try:
            results = self._db.similarity_search(query, k=k)
            return results
        except Exception:
            return []

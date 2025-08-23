from src.lib.langchain import LangChainClient
from langchain_text_splitters import CharacterTextSplitter
from src.schemas.docs_schema import DocsIndexingRequest, DocsType
from src.http.exceptions.docs_excpetions import InvalidFormatException
from src.config import Settings
from fastapi import UploadFile
import os


class DocsService:
    def __init__(self, db_file: str = Settings().db_file):
        self.client = LangChainClient(db_file=db_file)
        self.valid_extensions = {
            ".pdf": DocsType.PDF,
            ".docx": DocsType.DOCX,
            ".txt": DocsType.TXT,
            ".html": DocsType.HTML,
            ".htm": DocsType.HTML,
            ".md": DocsType.MD,
            ".markdown": DocsType.MD,
        }

    def _get_file_format(self, file: UploadFile) -> DocsType:
        if not file.filename:
            raise InvalidFormatException("Nome do arquivo não encontrado")

        filename_without_extension, file_extension = os.path.splitext(file.filename)
        file_extension = file_extension.lower()

        if file_extension not in self.valid_extensions:
            raise InvalidFormatException(file_extension)

        return self.valid_extensions[file_extension]

    async def indexa_documento(self, file: UploadFile, request: DocsIndexingRequest):
        content = await file.read()
        
        try:
            text = content.decode("utf-8")
        except Exception:
            text = str(content)
            
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = splitter.split_text(text)
        self.client.add_texts(docs)
        return None

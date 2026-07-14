import os
import re
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

class PaperProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
    
    def load_pdfs(self, pdf_paths):
        documents = []
        for path in pdf_paths:
            try:
                reader = PdfReader(path)
                text = ""
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if text.strip():
                    doc = Document(
                        page_content=text,
                        metadata={
                            "source": os.path.basename(path),
                            "pages": len(reader.pages),
                            "file_size": os.path.getsize(path)
                        }
                    )
                    documents.append(doc)
            except Exception as e:
                print(f"Error loading {path}: {e}")
        return documents
    
    def chunk_docs(self, documents):
        if not documents:
            return []
        chunks = self.splitter.split_documents(documents)
        # Add metadata to chunks
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = i
        return chunks
    
    def extract_metadata(self, documents):
        metadata = []
        for doc in documents:
            metadata.append({
                "source": doc.metadata.get("source", "Unknown"),
                "pages": doc.metadata.get("pages", 0),
                "characters": len(doc.page_content),
                "words": len(doc.page_content.split())
            })
        return metadata
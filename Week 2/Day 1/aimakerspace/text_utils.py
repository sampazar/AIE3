import os
from xml.dom.minidom import Document
import fitz #adding import of PyMuPDF to handle pdfs
from typing import List


class TextFileLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding
        print(f"Initialized with path: {self.path}")

    def load(self):
        print(f"Checking path: {self.path}")
        if os.path.isdir(self.path):
            print("Path is a directory.")
            self.load_directory()
        elif os.path.isfile(self.path):
            print(f"Path is a file with extension: {os.path.splitext(self.path)[-1]}")
            if self.path.endswith(".txt") or self.path.endswith(".pdf"): #added code to update 'load_file' method to handle '.txt
                print("Path is a valid .txt or .pdf file.")
                self.load_file()
            else:
                raise ValueError("Unsupported file format. Only .txt and .pdf files are supported.")
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .txt or .pdf file."
            )

    def load_file(self):
        #updating the 'load_file' method to handle pdf files
        print(f"Loading file: {self.path}")
        if self.path.endswith(".txt"):
            with open(self.path, "r", encoding=self.encoding) as f:
                self.documents.append(f.read())
        elif self.path.endswith(".pdf"):
            self._load_pdf()
        else:
            raise ValueError("Unsupported file format. Only .txt and .pdf files are supported.")
  
   #adding a new '_load_pdf' method to handle pdf files

    def _load_pdf(self):
        print(f"Loading pdf file: {self.path}")
        document = fitz.open(self.path)
        text = ""
        for page in document:
            text += page.get_text()
        self.documents.append(text)

    def load_directory(self):
        print(f"Loading directory: {self.path}")
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".txt"):
                    with open(
                        os.path.join(root, file), "r", encoding=self.encoding
                    ) as f:
                        self.documents.append(f.read())
                #adding code to handle pdf files
                elif file.endswith(".pdf"):
                    pdf_path = os.path.join(root, file)
                    self._load_pdf_path(pdf_path)
 
    def _load_pdf_path(self, pdf_path):
        print(f"Loading PDF from directory: {pdf_path}")
        document = fitz.open(pdf_path)
        text = ""
        for page in document:
            text += page.get_text()
        self.documents.append(text)

    def load_documents(self):
        self.load()
        return self.documents


class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks


if __name__ == "__main__":
    loader = TextFileLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])

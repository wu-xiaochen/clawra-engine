import logging
import hashlib
from abc import ABC, abstractmethod
from typing import List, Dict, Any

try:
    import chromadb
except ImportError:
    chromadb = None

logger = logging.getLogger(__name__)

class Document(ABC):
    """基本文档结构"""
    def __init__(self, content: str, metadata: Dict[str, Any] = None):
        self.content = content
        self.metadata = metadata or {}

class VectorStore(ABC):
    """
    向量存储抽象基类 (Vector Store Interface)
    """
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        pass
        
    @abstractmethod
    def similarity_search(self, query: str, top_k: int = 3) -> List[Document]:
        pass

class ChromaVectorStore(VectorStore):
    """
    Industrial-grade Vector Database (ChromaDB Integration)
    
    Uses ChromaDB as local vector storage, providing precise Embedding retrieval,
    combined with Neo4j graph traversal for true enterprise-grade Hybrid GraphRAG.
    """
    def __init__(self, persist_directory: str = "data/chroma_db", collection_name: str = "clawra_knowledge"):
        if chromadb is None:
            raise ImportError("chromadb is not installed. Please install it via `pip install chromadb`")
        
        # Use PersistentClient with anonymous tenant/database for compatibility
        try:
            # Use string literals for maximum compatibility across ChromaDB versions
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                tenant="default_tenant",
                database="default_database"
            )
        except Exception as e:
            # Fallback: try without tenant/database params for older ChromaDB versions
            logger.warning(f"ChromaDB initialization with tenant/database failed: {e}. Trying fallback.")
            try:
                self.client = chromadb.PersistentClient(path=persist_directory)
            except Exception as e2:
                logger.error(f"All ChromaDB initialization attempts failed: {e2}")
                # Last resort: use in-memory client
                self.client = chromadb.Client()
        
        
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
    def add_documents(self, documents: List[Document]) -> None:
        if not documents:
            return
            
        ids = [f"doc_{hashlib.md5(doc.content.encode()).hexdigest()}" for doc in documents]
        contents = [doc.content for doc in documents]
        metadatas = [doc.metadata if doc.metadata else {"source": "unknown"} for doc in documents]
        
        self.collection.add(
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"💾 ChromaVectorStore: Added {len(documents)} dense vectors.")

    def similarity_search(self, query: str, top_k: int = 3) -> List[Document]:
        if not self.collection.count():
            return []

        # Chroma query syntax returns dict of lists
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        docs = []
        if results and results.get("documents") and results["documents"][0]:
            for i in range(len(results["documents"][0])):
                content = results["documents"][0][i]
                metadata = results["metadatas"][0][i] if results.get("metadatas") else {}
                docs.append(Document(content=content, metadata=metadata))
                
        logger.info(f"🔍 ChromaVectorStore: Retrieved {len(docs)} semantic matches for query: '{query}'")
        return docs

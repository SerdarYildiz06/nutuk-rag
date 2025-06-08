#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def test_search():
    """Kayıtlı ChromaDB'de arama testi yapar."""
    
    print("🔍 ChromaDB Arama Testi Başlatılıyor...")
    
    try:
        # Embedding modelini yükle
        embedding_model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        print("✅ Embedding modeli yüklendi")
        
        # Kayıtlı ChromaDB'yi yükle
        persist_directory = "rag_chroma_db"
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
        
        print(f"✅ ChromaDB yüklendi: {persist_directory}")
        
        # Basit test sorgusu
        query = "Mustafa Kemal kimdir?"
        print(f"\n🔍 Test Sorgusu: {query}")
        
        # Arama yap
        results = vectorstore.similarity_search(query, k=2)
        
        print(f"✅ {len(results)} sonuç bulundu")
        
        for i, doc in enumerate(results, 1):
            print(f"\n--- Sonuç {i} ---")
            print(f"📄 Sayfa: {doc.metadata.get('page', 'Bilinmiyor')}")
            print(f"📝 İçerik: {doc.page_content[:200]}...")
            
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    test_search()

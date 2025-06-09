#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from rank_bm25 import BM25Okapi
import numpy as np
import re
import sys
import os
from typing import List, Tuple
import pickle

class ImprovedNutukRAGSystem:
    """İyileştirilmiş Nutuk belgeleri için RAG sistemi"""
    
    def __init__(self, model_name="qwen2:latest", rebuild_db=False):
        """RAG sistemini başlatır"""
        print("🚀 İyileştirilmiş Nutuk RAG Sistemi başlatılıyor...")
        
        # Ayarlar
        self.chunk_size = 300  # Daha küçük chunk boyutu
        self.chunk_overlap = 50
        self.persist_directory = "improved_rag_chroma_db"
        self.bm25_path = "bm25_index.pkl"
        
        # Daha iyi embedding modelini yükle
        print("📚 Gelişmiş embedding modeli yükleniyor...")
        embedding_model_name = "sentence-transformers/all-mpnet-base-v2"  # Daha güçlü model
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        print("✅ Embedding modeli yüklendi")
        
        # PDF'i yeniden işle veya mevcut DB'yi yükle
        if rebuild_db or not os.path.exists(self.persist_directory):
            print("🔄 PDF yeniden işleniyor...")
            self._rebuild_database()
        else:
            print("🗃️ Mevcut ChromaDB yükleniyor...")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            # BM25 indeksini yükle
            if os.path.exists(self.bm25_path):
                with open(self.bm25_path, 'rb') as f:
                    self.bm25, self.bm25_docs = pickle.load(f)
                print("✅ BM25 indeksi yüklendi")
            else:
                print("⚠️ BM25 indeksi bulunamadı, yeniden oluşturuluyor...")
                self._create_bm25_index()
        
        print("✅ ChromaDB yüklendi")
        
        # Ollama modelini yükle
        print(f"🤖 Ollama modeli ({model_name}) yükleniyor...")
        self.llm = OllamaLLM(model=model_name)
        print("✅ Ollama modeli yüklendi")
        
        # Gelişmiş prompt template'i oluştur
        self.prompt_template = ChatPromptTemplate.from_template("""
Sen Atatürk'ün Nutuk eseri konusunda uzman bir tarihçisin. Aşağıdaki belgeler kullanılarak soruyu detaylı ve açık bir şekilde yanıtla. 

Önemli kurallar:
- Belgelerde açık bir bilgi varsa, o bilgiyi tam olarak kullan
- Tarihleri, isimleri ve olayları olduğu gibi aktar
- Özellikle sayfa numaralarını belirt
- Mümkün olduğunca detaylı ve kapsamlı yanıt ver
- Eğer belgelerden tam yanıt bulamıyorsan, mevcut bilgileri kullanarak en iyi tahmini yap

Belgeler:
{context}

Soru: {question}

Yanıt: Verilen belgelere dayanarak,""")
        
        print("🎉 İyileştirilmiş RAG sistemi hazır!")
    
    def _rebuild_database(self):
        """PDF'i yeniden işleyerek veritabanını oluşturur"""
        pdf_path = "nutuk.pdf"
        if not os.path.exists(pdf_path):
            print(f"❌ {pdf_path} bulunamadı!")
            sys.exit(1)
        
        # PDF'i yükle
        print("📄 PDF yükleniyor...")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        # Daha küçük chunk'lara böl
        print("✂️ Belgeler küçük parçalara bölünüyor...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"✅ {len(chunks)} küçük parça oluşturuldu")
        
        # ChromaDB'ye kaydet
        print("💾 ChromaDB'ye kaydediliyor...")
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        # BM25 indeksini oluştur
        self._create_bm25_index()
        
        print("✅ Veritabanı oluşturuldu")
    
    def _create_bm25_index(self):
        """BM25 keyword arama indeksini oluşturur"""
        print("🔍 BM25 keyword arama indeksi oluşturuluyor...")
        
        # Tüm dokümanları al
        all_docs = self.vectorstore.get()
        texts = all_docs['documents']
        metadatas = all_docs['metadatas']
        
        # Metinleri tokenize et
        tokenized_texts = [self._tokenize_turkish(text) for text in texts]
        
        # BM25 indeksini oluştur
        self.bm25 = BM25Okapi(tokenized_texts)
        self.bm25_docs = [(text, meta) for text, meta in zip(texts, metadatas)]
        
        # Kaydet
        with open(self.bm25_path, 'wb') as f:
            pickle.dump((self.bm25, self.bm25_docs), f)
        
        print("✅ BM25 indeksi oluşturuldu")
    
    def _tokenize_turkish(self, text: str) -> List[str]:
        """Türkçe metin için tokenization"""
        # Küçük harfe çevir
        text = text.lower()
        
        # Türkçe karakterleri normalize et
        text = text.replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i')
        text = text.replace('ö', 'o').replace('ş', 's').replace('ü', 'u')
        
        # Sadece harf ve rakam bırak
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Tokenize et
        tokens = text.split()
        
        # Stop words'leri kaldır (temel Türkçe stop words)
        stop_words = {
            've', 'bir', 'bu', 'o', 'şu', 'de', 'da', 'den', 'dan', 'ile', 'için',
            'ne', 'ki', 'ya', 'yada', 'veya', 'ama', 'fakat', 'ancak', 'lakin',
            'gibi', 'kadar', 'sonra', 'önce', 'üzere', 'doğru', 'karşı', 'rağmen'
        }
        
        tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
        
        return tokens
    
    def semantic_search(self, query: str, k: int = 5) -> List[Document]:
        """Semantic similarity search"""
        results = self.vectorstore.similarity_search(query, k=k)
        return results
    
    def keyword_search(self, query: str, k: int = 5) -> List[Tuple[str, dict, float]]:
        """BM25 keyword search"""
        query_tokens = self._tokenize_turkish(query)
        scores = self.bm25.get_scores(query_tokens)
        
        # En yüksek skorlu k adet sonucu al
        top_indices = np.argsort(scores)[::-1][:k]
        
        results = []
        for idx in top_indices:
            if scores[idx] > 0:  # Sadece 0'dan büyük skorları al
                doc_text, metadata = self.bm25_docs[idx]
                results.append((doc_text, metadata, scores[idx]))
        
        return results
    
    def hybrid_search(self, query: str, k: int = 6) -> List[Document]:
        """Hibrit arama: semantic + keyword"""
        print(f"🔍 Hibrit arama yapılıyor: {query}")
        
        # Semantic arama
        semantic_results = self.semantic_search(query, k=k//2)
        
        # Keyword arama
        keyword_results = self.keyword_search(query, k=k//2)
        
        # Sonuçları birleştir
        all_results = []
        
        # Semantic sonuçları ekle
        for doc in semantic_results:
            all_results.append(doc)
        
        # Keyword sonuçlarını Document objesine çevir ve ekle
        for text, metadata, score in keyword_results:
            doc = Document(page_content=text, metadata=metadata)
            # Duplicate kontrolü
            is_duplicate = False
            for existing_doc in all_results:
                if existing_doc.page_content == doc.page_content:
                    is_duplicate = True
                    break
            if not is_duplicate:
                all_results.append(doc)
        
        print(f"✅ {len(all_results)} benzersiz sonuç bulundu")
        return all_results[:k]
    
    def rerank_results(self, query: str, documents: List[Document]) -> List[Document]:
        """Sonuçları yeniden sıralar"""
        query_lower = query.lower()
        query_tokens = set(self._tokenize_turkish(query))
        
        scored_docs = []
        for doc in documents:
            score = 0
            content_lower = doc.page_content.lower()
            content_tokens = set(self._tokenize_turkish(doc.page_content))
            
            # Exact match bonus
            if query_lower in content_lower:
                score += 10
            
            # Token overlap bonus
            overlap = len(query_tokens.intersection(content_tokens))
            score += overlap * 2
            
            # Length penalty (çok kısa metinleri cezalandır)
            if len(doc.page_content) < 50:
                score -= 2
            
            scored_docs.append((doc, score))
        
        # Skora göre sırala
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        return [doc for doc, score in scored_docs]
    
    def search_documents(self, query: str, k: int = 6):
        """Gelişmiş arama: hibrit + reranking"""
        # Hibrit arama
        results = self.hybrid_search(query, k=k*2)  # Daha fazla sonuç al
        
        # Reranking
        if results:
            results = self.rerank_results(query, results)
        
        # En iyi k sonucu döndür
        return results[:k]
    
    def generate_answer(self, question: str, context_docs: List[Document]) -> str:
        """LLM ile yanıt üretir"""
        # Belgeleri sayfa numarasına göre sırala
        context_docs = sorted(context_docs, key=lambda x: x.metadata.get('page', 0))
        
        # Belgeleri tek bir metin haline getir
        context = "\n\n".join([
            f"Sayfa {doc.metadata.get('page', '?')}: {doc.page_content}" 
            for doc in context_docs
        ])
        
        # Prompt'u oluştur
        formatted_prompt = self.prompt_template.format(
            context=context, 
            question=question
        )
        
        print("🤖 Ollama ile yanıt üretiliyor...")
        response = self.llm.invoke(formatted_prompt)
        return response
    
    def ask(self, question: str, k: int = 6):
        """Tam RAG işlemi: gelişmiş arama + yanıt üretme"""
        print(f"\n{'='*70}")
        print(f"❓ Soru: {question}")
        print(f"{'='*70}")
        
        # 1. Gelişmiş arama
        context_docs = self.search_documents(question, k=k)
        
        if not context_docs:
            return "❌ İlgili belge bulunamadı."
        
        # 2. Bulunan belgeleri göster
        print("\n📄 Bulunan belgeler:")
        for i, doc in enumerate(context_docs, 1):
            page = doc.metadata.get('page', '?')
            content_preview = doc.page_content[:150].replace('\n', ' ')
            print(f"  {i}. Sayfa {page}: {content_preview}...")
        
        # 3. LLM ile yanıt üret
        answer = self.generate_answer(question, context_docs)
        
        print(f"\n💬 Yanıt:\n{answer}")
        print(f"\n{'='*70}")
        
        return answer

def main():
    """Ana fonksiyon - interaktif soru-cevap"""
    try:
        # Kullanıcıya seçenek sun
        print("🔧 Veritabanını yeniden oluşturmak ister misiniz? (y/n): ", end="")
        rebuild = input().strip().lower() in ['y', 'yes', 'evet', 'e']
        
        # RAG sistemini başlat
        rag = ImprovedNutukRAGSystem(rebuild_db=rebuild)
        
        print("\n🎯 İyileştirilmiş Nutuk RAG Sistemi hazır!")
        print("💡 Nutuk hakkında soru sorabilirsiniz.")
        print("💡 Özellikler: Hibrit arama, küçük chunk'lar, reranking")
        print("💡 Çıkmak için 'q' yazın.\n")
        
        while True:
            try:
                question = input("❓ Sorunuz: ").strip()
                
                if question.lower() in ['q', 'quit', 'exit', 'çık']:
                    print("👋 Görüşürüz!")
                    break
                
                if not question:
                    continue
                
                # Soruyu yanıtla
                rag.ask(question)
                
            except KeyboardInterrupt:
                print("\n👋 Görüşürüz!")
                break
            except Exception as e:
                print(f"❌ Hata: {e}")
                
    except Exception as e:
        print(f"❌ Sistem başlatılamadı: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

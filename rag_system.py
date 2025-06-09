#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
import sys

class NutukRAGSystem:
    """Nutuk belgeleri için RAG sistemi"""
    
    def __init__(self, model_name="qwen2:latest"):
        """RAG sistemini başlatır"""
        print("🚀 Nutuk RAG Sistemi başlatılıyor...")
        
        # Embedding modelini yükle
        print("📚 Embedding modeli yükleniyor...")
        embedding_model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        print("✅ Embedding modeli yüklendi")
        
        # ChromaDB'yi yükle
        print("🗃️ ChromaDB yükleniyor...")
        persist_directory = "rag_chroma_db"
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )
        print("✅ ChromaDB yüklendi")
        
        # Ollama modelini yükle
        print(f"🤖 Ollama modeli ({model_name}) yükleniyor...")
        self.llm = OllamaLLM(model=model_name)
        print("✅ Ollama modeli yüklendi")
        
        # Prompt template'i oluştur
        self.prompt_template = ChatPromptTemplate.from_template("""
Sen Atatürk'ün Nutuk eseri konusunda uzman bir tarihçisin. Aşağıdaki belgeler kullanılarak soruyu detaylı ve açık bir şekilde yanıtla. 

Önemli kurallar:
- Belgelerde açık bir bilgi varsa, o bilgiyi tam olarak kullan
- Tarihleri, isimleri ve olayları olduğu gibi aktar
- Eğer belgelerden tam yanıt bulamıyorsan, "Bu konuda belgede yeterli bilgi bulunmuyor" de
- Hangi sayfalardan bilgi aldığını belirt

Belgeler:
{context}

Soru: {question}

Yanıt: Verilen belgelere dayanarak,""")
        
        print("🎉 RAG sistemi hazır!")
    
    def search_documents(self, query, k=3):
        """Vektör veritabanında arama yapar"""
        print(f"🔍 Arama yapılıyor: {query}")
        results = self.vectorstore.similarity_search(query, k=k)
        print(f"✅ {len(results)} sonuç bulundu")
        return results
    
    def generate_answer(self, question, context_docs):
        """LLM ile yanıt üretir"""
        # Belgeleri tek bir metin haline getir
        context = "\n\n".join([f"Sayfa {doc.metadata.get('page', '?')}: {doc.page_content}" 
                               for doc in context_docs])
        
        # Prompt'u oluştur
        formatted_prompt = self.prompt_template.format(
            context=context, 
            question=question
        )
        
        print("🤖 Ollama ile yanıt üretiliyor...")
        response = self.llm.invoke(formatted_prompt)
        return response
    
    def ask(self, question, k=3):
        """Tam RAG işlemi: arama + yanıt üretme"""
        print(f"\n{'='*60}")
        print(f"❓ Soru: {question}")
        print(f"{'='*60}")
        
        # 1. İlgili belgeleri bul
        context_docs = self.search_documents(question, k=k)
        
        if not context_docs:
            return "❌ İlgili belge bulunamadı."
        
        # 2. Bulunan belgeleri göster
        print("\n📄 Bulunan belgeler:")
        for i, doc in enumerate(context_docs, 1):
            print(f"  {i}. Sayfa {doc.metadata.get('page', '?')}: {doc.page_content[:100]}...")
        
        # 3. LLM ile yanıt üret
        answer = self.generate_answer(question, context_docs)
        
        print(f"\n💬 Yanıt:\n{answer}")
        print(f"\n{'='*60}")
        
        return answer

def main():
    """Ana fonksiyon - interaktif soru-cevap"""
    try:
        # RAG sistemini başlat
        rag = NutukRAGSystem()
        
        print("\n🎯 Nutuk RAG Sistemi hazır!")
        print("💡 Nutuk hakkında soru sorabilirsiniz.")
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

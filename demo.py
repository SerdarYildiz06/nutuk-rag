#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nutuk RAG Sistemi - Örnek Kullanım Kılavuzu

Bu script, RAG sisteminin nasıl kullanılacağını gösterir.
"""

from rag_system import NutukRAGSystem

def demo_rag_system():
    """RAG sisteminin demo kullanımı"""
    print("🎯 Nutuk RAG Sistemi Demo")
    print("=" * 50)
    
    # 1. RAG sistemini başlat
    print("\n1️⃣ RAG Sistemi Başlatılıyor...")
    rag = NutukRAGSystem()
    
    # 2. Örnek sorular
    demo_questions = [
        "Mustafa Kemal Atatürk kimdir?",
        "Kurtuluş Savaşı ne zaman başladı?",
        "TBMM hangi tarihte kuruldu?",
        "Milli Mücadele'nin amacı neydi?",
        "İzmir'in işgali nasıl gerçekleşti?"
    ]
    
    print(f"\n2️⃣ Demo Sorular ({len(demo_questions)} adet)")
    print("-" * 30)
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n🔹 Demo {i}: {question}")
        input("   ⏸️  Devam etmek için Enter'a basın...")
        
        # Soruyu sor
        rag.ask(question, k=2)
        
        print("\n" + "🔹" * 40)
    
    print("\n✅ Demo tamamlandı!")
    print("\n💡 İpucu: Kendi sorularınızı sormak için 'python rag_system.py' komutunu kullanın")

def simple_question_example():
    """Basit soru örneği"""
    print("\n🎯 Basit Kullanım Örneği")
    print("=" * 30)
    
    # RAG sistemini başlat
    rag = NutukRAGSystem()
    
    # Tek bir soru sor
    question = "Nutuk'ta hangi konular ele alınmıştır?"
    print(f"\n❓ Soru: {question}")
    
    # Yanıt al
    answer = rag.ask(question)
    
    return answer

def advanced_search_example():
    """Gelişmiş arama örneği"""
    print("\n🎯 Gelişmiş Arama Örneği")
    print("=" * 30)
    
    # RAG sistemini başlat
    rag = NutukRAGSystem()
    
    # Sadece arama yap (LLM kullanmadan)
    query = "Ankara"
    print(f"\n🔍 Sadece arama: {query}")
    
    docs = rag.search_documents(query, k=5)
    
    print(f"📄 Bulunan {len(docs)} belge:")
    for i, doc in enumerate(docs, 1):
        print(f"\n{i}. Sayfa {doc.metadata.get('page', '?')}")
        print(f"   📝 {doc.page_content[:200]}...")
    
    return docs

if __name__ == "__main__":
    print("🚀 Nutuk RAG Sistemi - Örnek Kullanımlar")
    print("=" * 60)
    
    while True:
        print("\n📋 Seçenekler:")
        print("1. 🎬 Full Demo (5 örnek soru)")
        print("2. 🎯 Basit Kullanım")
        print("3. 🔍 Gelişmiş Arama")
        print("4. 🚪 Çıkış")
        
        choice = input("\n🎯 Seçiminiz (1-4): ").strip()
        
        if choice == "1":
            demo_rag_system()
        elif choice == "2":
            simple_question_example()
        elif choice == "3":
            advanced_search_example()
        elif choice == "4":
            print("👋 Görüşürüz!")
            break
        else:
            print("❌ Geçersiz seçim. Lütfen 1-4 arası bir sayı girin.")
        
        input("\n⏸️  Ana menüye dönmek için Enter'a basın...")
        print("\n" + "="*60)

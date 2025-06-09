#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from improved_rag_system import ImprovedNutukRAGSystem
import time

def quick_test():
    """Hızlı test - İzmir işgali sorusu"""
    print("🚀 Hızlı Test - İyileştirilmiş RAG Sistemi")
    print("="*60)
    
    # Test sorusu
    test_question = "İzmir'in işgali nasıl gerçekleşti?"
    print(f"❓ Test Sorusu: {test_question}")
    print("="*60)
    
    # Sistem yükleme
    print("\n1️⃣ Sistem yükleniyor...")
    start_time = time.time()
    
    try:
        # Mevcut veritabanını kullan
        rag = ImprovedNutukRAGSystem(rebuild_db=False)
        
        load_time = time.time() - start_time
        print(f"✅ Sistem yüklendi ({load_time:.2f}s)")
        
        # Soru sorma
        print("\n2️⃣ Soru yanıtlanıyor...")
        start_time = time.time()
        
        answer = rag.ask(test_question, k=6)
        
        answer_time = time.time() - start_time
        print(f"✅ Yanıt alındı ({answer_time:.2f}s)")
        
        # Özet
        print(f"\n{'='*60}")
        print("📊 HIZLI TEST ÖZETİ")
        print(f"{'='*60}")
        print(f"⏱️ Sistem yükleme: {load_time:.2f}s")
        print(f"⏱️ Yanıt süresi: {answer_time:.2f}s")
        print(f"⏱️ Toplam süre: {(load_time + answer_time):.2f}s")
        print(f"✅ Test başarılı!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test başarısız: {e}")
        return False

def search_only_test():
    """Sadece arama testi"""
    print("\n🔍 Arama Testi")
    print("="*40)
    
    try:
        rag = ImprovedNutukRAGSystem(rebuild_db=False)
        
        test_queries = [
            "İzmir işgali",
            "TBMM kuruluş",
            "Mustafa Kemal",
            "Kurtuluş Savaşı",
            "Sakarya Savaşı"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Arama: {query}")
            start_time = time.time()
            
            results = rag.search_documents(query, k=3)
            
            search_time = time.time() - start_time
            print(f"⏱️ {search_time:.2f}s | 📄 {len(results)} sonuç")
            
            for i, doc in enumerate(results[:2], 1):
                page = doc.metadata.get('page', '?')
                preview = doc.page_content[:100].replace('\n', ' ')
                print(f"  {i}. Sayfa {page}: {preview}...")
        
        print("\n✅ Arama testleri tamamlandı")
        return True
        
    except Exception as e:
        print(f"❌ Arama testi başarısız: {e}")
        return False

if __name__ == "__main__":
    print("🧪 İyileştirilmiş RAG Sistemi - Hızlı Test\n")
    
    # Ana test
    success1 = quick_test()
    
    # Arama testi
    success2 = search_only_test()
    
    print(f"\n{'='*60}")
    print("🎯 GENEL SONUÇ")
    print(f"{'='*60}")
    print(f"✅ Ana test: {'BAŞARILI' if success1 else 'BAŞARISIZ'}")
    print(f"✅ Arama testi: {'BAŞARILI' if success2 else 'BAŞARISIZ'}")
    
    if success1 and success2:
        print("🎉 Tüm testler başarılı! Sistem kullanıma hazır.")
    else:
        print("⚠️ Bazı testler başarısız. Sistem kontrolü gerekli.")

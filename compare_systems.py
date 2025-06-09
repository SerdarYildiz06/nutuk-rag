#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import os

def test_izmir_question():
    """İzmir işgali sorusunu her iki sistemle test et"""
    question = "İzmir'in işgali nasıl gerçekleşti?"
    
    print("🆚 SİSTEM KARŞILAŞTIRMA TESTİ")
    print("="*60)
    print(f"❓ Test Sorusu: {question}")
    print("="*60)
    
    # İyileştirilmiş sistem testi
    print("\n🚀 İYİLEŞTİRİLMİŞ SİSTEM TEST EDİLİYOR...")
    print("-" * 50)
    
    try:
        from improved_rag_system import ImprovedNutukRAGSystem
        
        start_time = time.time()
        improved_rag = ImprovedNutukRAGSystem(rebuild_db=False)
        load_time = time.time() - start_time
        
        start_time = time.time()
        improved_docs = improved_rag.search_documents(question, k=6)
        search_time = time.time() - start_time
        
        print(f"⏱️ Yükleme süresi: {load_time:.2f}s")
        print(f"⏱️ Arama süresi: {search_time:.2f}s")
        print(f"📄 Bulunan belge sayısı: {len(improved_docs)}")
        
        if improved_docs:
            print("\n📖 Bulunan sayfalar:")
            for i, doc in enumerate(improved_docs[:3], 1):
                page = doc.metadata.get('page', '?')
                preview = doc.page_content[:100].replace('\n', ' ')
                print(f"  {i}. Sayfa {page}: {preview}...")
            
            improved_has_33 = any(doc.metadata.get('page') == 33 for doc in improved_docs)
            print(f"✅ Sayfa 33 bulundu: {'EVET' if improved_has_33 else 'HAYIR'}")
        else:
            print("❌ Hiç belge bulunamadı")
            improved_has_33 = False
            
    except Exception as e:
        print(f"❌ İyileştirilmiş sistem hatası: {e}")
        improved_has_33 = False
        load_time = search_time = 0
    
    # Eski sistem testi
    print(f"\n📟 ESKİ SİSTEM TEST EDİLİYOR...")
    print("-" * 50)
    
    try:
        from rag_system import NutukRAGSystem
        
        start_time = time.time()
        old_rag = NutukRAGSystem()
        old_load_time = time.time() - start_time
        
        start_time = time.time()
        old_docs = old_rag.search_documents(question, k=3)
        old_search_time = time.time() - start_time
        
        print(f"⏱️ Yükleme süresi: {old_load_time:.2f}s")
        print(f"⏱️ Arama süresi: {old_search_time:.2f}s")
        print(f"📄 Bulunan belge sayısı: {len(old_docs)}")
        
        if old_docs:
            print("\n📖 Bulunan sayfalar:")
            for i, doc in enumerate(old_docs, 1):
                page = doc.metadata.get('page', '?')
                preview = doc.page_content[:100].replace('\n', ' ')
                print(f"  {i}. Sayfa {page}: {preview}...")
            
            old_has_33 = any(doc.metadata.get('page') == 33 for doc in old_docs)
            print(f"✅ Sayfa 33 bulundu: {'EVET' if old_has_33 else 'HAYIR'}")
        else:
            print("❌ Hiç belge bulunamadı")
            old_has_33 = False
            
    except Exception as e:
        print(f"❌ Eski sistem hatası: {e}")
        old_has_33 = False
        old_load_time = old_search_time = 0
    
    # Karşılaştırma özeti
    print(f"\n{'='*60}")
    print("📊 KARŞILAŞTIRMA ÖZETİ")
    print(f"{'='*60}")
    
    print(f"🎯 Sayfa 33 Bulma:")
    print(f"  • İyileştirilmiş: {'✅ BAŞARILI' if improved_has_33 else '❌ BAŞARISIZ'}")
    print(f"  • Eski Sistem:   {'✅ BAŞARILI' if old_has_33 else '❌ BAŞARISIZ'}")
    
    print(f"\n⏱️ Performans:")
    print(f"  • İyileştirilmiş: {load_time + search_time:.2f}s")
    print(f"  • Eski Sistem:   {old_load_time + old_search_time:.2f}s")
    
    if improved_has_33 and not old_has_33:
        print(f"\n🎉 SONUÇ: İyileştirilmiş sistem başarılı!")
        print(f"🔍 İzmir işgali konusunda Sayfa 33'ü bulabildi.")
    elif old_has_33 and not improved_has_33:
        print(f"\n⚠️ SONUÇ: Eski sistem daha başarılı.")
    elif improved_has_33 and old_has_33:
        print(f"\n✅ SONUÇ: Her iki sistem de başarılı.")
    else:
        print(f"\n❌ SONUÇ: Her iki sistem de başarısız.")

if __name__ == "__main__":
    test_izmir_question()

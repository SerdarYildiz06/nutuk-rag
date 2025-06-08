#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rag_system import NutukRAGSystem

def test_rag_batch():
    """RAG sistemini otomatik test eder"""
    print("🧪 RAG Sistemi Batch Test")
    print("=" * 50)
    
    # RAG sistemini başlat
    rag = NutukRAGSystem()
    
    # Test soruları
    test_questions = [
        "Mustafa Kemal kimdir?",
        "Kurtuluş Savaşı nasıl başladı?",
        "TBMM ne zaman kuruldu?",
        "Milli Mücadele nedir?",
        "Türk milleti neden mücadele etti?",
        "Ankara hangi durumda bulunuyordu?",
        "Milli birlik nasıl sağlandı?",
        "Nutuk'ta hangi olaylar anlatılır?",
        "İzmir işgali nasıl gerçekleşti?",
        "Yunan kuvvetleri nerede bulunuyordu?"
    ]
    
    print(f"\n🔍 {len(test_questions)} soru test edilecek...\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Test {i}/{len(test_questions)}")
        print("-" * 40)
        
        try:
            # Soruyu sor ve yanıt al
            answer = rag.ask(question, k=2)  # Daha hızlı test için k=2
            
        except Exception as e:
            print(f"❌ Hata: {e}")
        
        print("\n" + "="*60)
    
    print("\n✅ Tüm testler tamamlandı!")

if __name__ == "__main__":
    test_rag_batch()

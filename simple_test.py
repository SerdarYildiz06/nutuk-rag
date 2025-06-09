#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from improved_rag_system import ImprovedNutukRAGSystem
import sys

def main():
    """Terminal input sorunu olmadan test"""
    print("🧪 İyileştirilmiş RAG Sistemi - Manuel Test")
    print("="*50)
    
    try:
        # Sistem yükleme
        print("1️⃣ Sistem yükleniyor...")
        rag = ImprovedNutukRAGSystem(rebuild_db=False)
        
        # Test soruları
        test_questions = [
            "İzmir'in işgali nasıl gerçekleşti?",
            "TBMM ne zaman kuruldu?",
            "Mustafa Kemal Atatürk kimdir?",
            "Kurtuluş Savaşı'nın amacı neydi?"
        ]
        
        print(f"\n2️⃣ {len(test_questions)} soru test edilecek...")
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n{'='*60}")
            print(f"Test {i}: {question}")
            print(f"{'='*60}")
            
            try:
                answer = rag.ask(question, k=6)
                print("✅ Test başarılı")
            except Exception as e:
                print(f"❌ Test hatası: {e}")
        
        print(f"\n{'='*60}")
        print("🎉 Tüm testler tamamlandı!")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"❌ Sistem hatası: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

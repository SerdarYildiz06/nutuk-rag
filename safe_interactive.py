#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from improved_rag_system import ImprovedNutukRAGSystem
import sys

def interactive_test():
    """Input sorunu olmadan interaktif test"""
    print("🎯 İyileştirilmiş Nutuk RAG - İnteraktif Test")
    print("="*50)
    
    try:
        # Sistem yükleme
        print("🚀 Sistem yükleniyor...")
        rag = ImprovedNutukRAGSystem(rebuild_db=False)
        print("✅ Sistem hazır!")
        
        # Örnek sorular
        example_questions = [
            "İzmir'in işgali nasıl gerçekleşti?",
            "TBMM ne zaman kuruldu?", 
            "Mustafa Kemal Atatürk kimdir?",
            "Kurtuluş Savaşı'nın amacı neydi?",
            "Sakarya Savaşı'nın önemi nedir?",
            "Mondros Mütarekesi ne zaman imzalandı?"
        ]
        
        print(f"\n📚 Örnek sorular:")
        for i, q in enumerate(example_questions, 1):
            print(f"  {i}. {q}")
        
        print(f"\n💡 Soru numarası girin (1-{len(example_questions)}) veya 'q' ile çıkın:")
        
        while True:
            try:
                # Güvenli input alma
                choice = sys.stdin.readline().strip()
                
                if choice.lower() in ['q', 'quit', 'exit', 'çık']:
                    print("👋 Görüşürüz!")
                    break
                
                if choice.isdigit():
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(example_questions):
                        question = example_questions[choice_num - 1]
                        print(f"\n🔍 Seçilen soru: {question}")
                        
                        # Soruyu yanıtla
                        answer = rag.ask(question, k=6)
                        
                        print(f"\n💡 Başka bir soru numarası girin (1-{len(example_questions)}) veya 'q' ile çıkın:")
                    else:
                        print(f"❌ Lütfen 1-{len(example_questions)} arası bir sayı girin!")
                else:
                    print(f"❌ Lütfen geçerli bir sayı (1-{len(example_questions)}) veya 'q' girin!")
                        
            except EOFError:
                print("\n👋 Çıkış yapılıyor...")
                break
            except Exception as e:
                print(f"❌ Hata: {e}")
                
    except Exception as e:
        print(f"❌ Sistem hatası: {e}")
        sys.exit(1)

def quick_demo():
    """Hızlı demo - tüm soruları otomatik test et"""
    print("⚡ Hızlı Demo - Otomatik Test")
    print("="*40)
    
    try:
        rag = ImprovedNutukRAGSystem(rebuild_db=False)
        
        questions = [
            "İzmir işgali",
            "TBMM kuruluş", 
            "Atatürk kimdir"
        ]
        
        for q in questions:
            print(f"\n🔍 Test: {q}")
            answer = rag.ask(q, k=3)
            print("✅ Başarılı")
            
        print("\n🎉 Demo tamamlandı!")
        
    except Exception as e:
        print(f"❌ Demo hatası: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        quick_demo()
    else:
        interactive_test()

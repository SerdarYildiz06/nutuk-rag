#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 Nutuk RAG - Hızlı Başlangıç

Ollama'yı indirdiniz, şimdi RAG sistemi ile Nutuk üzerinde 
akıllı soru-cevap yapabilirsiniz!
"""

import sys
from rag_system import NutukRAGSystem

def quick_start():
    """Hızlı başlangıç demo"""
    
    print("🇹🇷 Nutuk RAG Sistemi - Hızlı Başlangıç")
    print("=" * 50)
    
    print("\n✨ Ollama ile RAG sistemi kuruldu!")
    print("📚 Atatürk'ün Nutuk'u işlendi")
    print("🤖 Yapay zeka yanıtları hazır")
    
    try:
        # RAG sistemini başlat
        print("\n🔄 Sistem başlatılıyor...")
        rag = NutukRAGSystem()
        
        # Örnek soru sor
        question = "Mustafa Kemal Atatürk kimdir?"
        print(f"\n🎯 Örnek soru: {question}")
        print("⏳ Yanıt hazırlanıyor...")
        
        answer = rag.ask(question, k=2)
        
        print("\n🎉 Başarılı! Sistem hazır.")
        print("\n📋 Şimdi ne yapabilirsiniz:")
        print("1. 💬 Terminal: python rag_system.py")
        print("2. 🌐 Web Arayüzü: python web_app.py")
        print("3. 🧪 Batch Test: python batch_test.py") 
        print("4. 🎬 Demo: python demo.py")
        
        # İnteraktif devam
        print("\n" + "="*50)
        choice = input("💡 İnteraktif soru-cevap başlatmak ister misiniz? (e/h): ").strip().lower()
        
        if choice in ['e', 'evet', 'y', 'yes']:
            interactive_session(rag)
        else:
            print("👋 README.md dosyasına bakarak diğer özellikleri keşfedebilirsiniz!")
            
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        print("\n🔧 Sorun giderme:")
        print("1. Ollama çalışıyor mu? → ollama list")
        print("2. Gerekli paketler kurulu mu? → pip install -r requirements.txt")
        print("3. ChromaDB var mı? → ls rag_chroma_db/")
        sys.exit(1)

def interactive_session(rag):
    """Basit interaktif oturum"""
    print("\n🎮 İnteraktif Soru-Cevap Başlatıldı")
    print("💡 Çıkmak için 'q' yazın")
    print("-" * 40)
    
    örnek_sorular = [
        "TBMM ne zaman kuruldu?",
        "Kurtuluş Savaşı nasıl başladı?",
        "İzmir işgali nasıl gerçekleşti?",
        "Milli Mücadele'nin amacı neydi?",
        "Ankara hangi durumda bulunuyordu?"
    ]
    
    print(f"\n💡 Örnek sorular:")
    for i, soru in enumerate(örnek_sorular[:3], 1):
        print(f"   {i}. {soru}")
    print("   ...")
    
    soru_sayısı = 0
    
    while True:
        try:
            soru = input(f"\n❓ Soru {soru_sayısı + 1}: ").strip()
            
            if soru.lower() in ['q', 'quit', 'exit', 'çık']:
                break
                
            if not soru:
                continue
                
            # Soruyu yanıtla
            rag.ask(soru, k=2)
            soru_sayısı += 1
            
            if soru_sayısı >= 3:
                devam = input("\n💭 Devam etmek istiyor musunuz? (e/h): ").strip().lower()
                if devam not in ['e', 'evet', 'y', 'yes']:
                    break
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    print(f"\n🎯 Toplam {soru_sayısı} soru soruldu")
    print("👋 Teşekkürler! Diğer özellikleri de deneyin:")
    print("   🌐 Web: python web_app.py")
    print("   📊 Batch: python batch_test.py")

if __name__ == "__main__":
    quick_start()

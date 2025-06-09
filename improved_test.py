#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rag_system import NutukRAGSystem

def improved_search_test():
    """İyileştirilmiş arama testi"""
    
    print("🔬 İzmir İşgali - İyileştirilmiş Arama Testi")
    print("="*60)
    
    # RAG sistemini başlat
    rag = NutukRAGSystem()
    
    # En iyi sonuç veren arama terimi
    question = "İzmir Yunan işgali 1919 15 Mayıs nasıl gerçekleşti"
    
    print(f"❓ Optimize Edilmiş Soru: {question}")
    print("="*60)
    
    # Tam RAG işlemi
    answer = rag.ask(question, k=5)
    
    print("\n" + "="*60)
    print("🎯 SONUÇ: Sayfa 33'teki kritik bilgiler yakalandı mı?")
    print("📋 Kontrol Listesi:")
    print("  □ 13 Mayıs'tan beri emareler")
    print("  □ 14/15 Mayıs gecesi toplantı") 
    print("  □ Reddi İlhak prensibi")
    print("  □ Yahudi mezarlığında miting")
    print("  □ 15 Mayıs sabahı Yunan askerleri rıhtımda")

if __name__ == "__main__":
    improved_search_test()

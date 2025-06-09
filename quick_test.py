#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rag_system import NutukRAGSystem

def quick_izmir_test():
    """Hızlı İzmir testi"""
    
    try:
        rag = NutukRAGSystem()
        
        # Optimize edilmiş soru
        question = "İzmir Yunan işgali 1919"
        print(f"Soru: {question}")
        
        # Daha fazla sonuçla ara
        answer = rag.ask(question, k=8)
        
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    quick_izmir_test()

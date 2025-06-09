#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from improved_rag_system import ImprovedNutukRAGSystem
import time

def test_improved_system():
    """İyileştirilmiş sistemi test eder"""
    print("🧪 İyileştirilmiş RAG sistemi test ediliyor...\n")
    
    # Sistemi başlat (yeniden oluşturma seçeneği ile)
    rag = ImprovedNutukRAGSystem(rebuild_db=True)
    
    # Test soruları
    test_questions = [
        "İzmir'in işgali nasıl gerçekleşti?",
        "Mustafa Kemal Atatürk kimdir?",
        "TBMM ne zaman kuruldu?",
        "Kurtuluş Savaşı'nın amacı neydi?",
        "Ankara'nın durumu nasıldı?",
        "Milli Mücadele nedir?",
        "İtilaf Devletleri kimlerdir?",
        "Mondros Mütarekesi ne zaman imzalandı?",
        "Sevr Antlaşması'nın hükümleri nelerdi?",
        "Sakarya Savaşı'nın önemi nedir?"
    ]
    
    print(f"📝 {len(test_questions)} soru test edilecek...\n")
    
    results = []
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*80}")
        print(f"🔍 Test {i}/{len(test_questions)}: {question}")
        print(f"{'='*80}")
        
        start_time = time.time()
        
        try:
            # Soruyu yanıtla
            answer = rag.ask(question, k=6)
            
            end_time = time.time()
            duration = end_time - start_time
            
            results.append({
                'question': question,
                'answer': answer,
                'duration': duration,
                'success': True
            })
            
            print(f"\n⏱️ Süre: {duration:.2f} saniye")
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"❌ Hata: {e}")
            
            results.append({
                'question': question,
                'answer': None,
                'duration': duration,
                'success': False,
                'error': str(e)
            })
        
        # Kısa bekleme
        time.sleep(1)
    
    # Özet rapor
    print(f"\n{'='*80}")
    print("📊 TEST ÖZET RAPORU")
    print(f"{'='*80}")
    
    successful = sum(1 for r in results if r['success'])
    total_time = sum(r['duration'] for r in results)
    avg_time = total_time / len(results)
    
    print(f"✅ Başarılı: {successful}/{len(results)}")
    print(f"⏱️ Toplam süre: {total_time:.2f} saniye")
    print(f"⏱️ Ortalama süre: {avg_time:.2f} saniye")
    
    if successful < len(results):
        print("\n❌ Başarısız testler:")
        for r in results:
            if not r['success']:
                print(f"  - {r['question']}: {r.get('error', 'Bilinmeyen hata')}")
    
    return results

def compare_with_old_system():
    """Eski sistem ile karşılaştırma yapar"""
    print("\n🔄 Eski sistem ile karşılaştırma yapılıyor...\n")
    
    # Test sorusu
    test_question = "İzmir'in işgali nasıl gerçekleşti?"
    
    print("🆚 Karşılaştırma Testi")
    print(f"Soru: {test_question}\n")
    
    # İyileştirilmiş sistem
    print("🚀 İYİLEŞTİRİLMİŞ SİSTEM:")
    improved_rag = ImprovedNutukRAGSystem()
    
    start_time = time.time()
    improved_answer = improved_rag.ask(test_question, k=6)
    improved_time = time.time() - start_time
    
    print(f"⏱️ Süre: {improved_time:.2f} saniye\n")
    
    # Eski sistem
    print("📟 ESKİ SİSTEM:")
    from rag_system import NutukRAGSystem
    old_rag = NutukRAGSystem()
    
    start_time = time.time()
    old_answer = old_rag.ask(test_question, k=3)
    old_time = time.time() - start_time
    
    print(f"⏱️ Süre: {old_time:.2f} saniye\n")
    
    # Karşılaştırma özeti
    print(f"{'='*80}")
    print("📊 KARŞILAŞTIRMA ÖZETİ")
    print(f"{'='*80}")
    print(f"⏱️ İyileştirilmiş sistem: {improved_time:.2f}s")
    print(f"⏱️ Eski sistem: {old_time:.2f}s")
    print(f"📈 Hız farkı: {((old_time - improved_time) / old_time * 100):.1f}% {'hızlandı' if improved_time < old_time else 'yavaşladı'}")

if __name__ == "__main__":
    # Ana test
    results = test_improved_system()
    
    # Karşılaştırma testi
    try:
        compare_with_old_system()
    except Exception as e:
        print(f"❌ Karşılaştırma yapılamadı: {e}")
    
    print("\n🎉 Testler tamamlandı!")

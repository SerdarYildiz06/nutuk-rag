# Nutuk RAG Sistemi - Kullanım Kılavuzu

## 🎯 Ne Yapıyor?

Bu sistem, Atatürk'ün **Nutuk** eseri üzerinde **RAG (Retrieval-Augmented Generation)** teknolojisi kullanarak akıllı soru-cevap hizmeti sunar.

- 📚 **Nutuk** PDF'inden vektör veritabanı oluşturur
- 🔍 Sorularınızla ilgili metinleri bulur
- 🤖 **Ollama** ile yanıtlar üretir
- 📄 Kaynak sayfa bilgilerini gösterir

## 🚀 Kurulum

### 1. Gereksinimler

```bash
# Python 3.8+ gerekli
# Ollama kurulu olmalı (https://ollama.ai)
```

### 2. Paket Kurulumu

```bash
# Sanal ortamı aktive et
source myenv/bin/activate

# Gerekli paketler zaten kurulu
# Eksik varsa: pip install -r requirements.txt
```

### 3. Ollama Model İndirme

```bash
# Qwen2 modelini indir (4.4GB)
ollama pull qwen2

# Alternatif modeller:
# ollama pull llama3
# ollama pull mistral
```

## 📁 Dosya Yapısı

```
nutuk-rag/
├── rag_system.py      # Ana RAG sistemi
├── web_app.py         # Web arayüzü
├── batch_test.py      # Toplu test
├── demo.py           # Örnek kullanımlar
├── test_search.py    # Arama testi
├── nutuk.pdf         # Kaynak belge
├── rag_chroma_db/    # Vektör veritabanı
└── templates/        # Web şablonları
```

## 🎮 Kullanım Yöntemleri

### 1. 💬 Terminal (İnteraktif)

```bash
python rag_system.py
```

- Soru sorun, yanıt alın
- `q` ile çıkış

### 2. 🌐 Web Arayüzü

```bash
python web_app.py
```

- http://localhost:8000 açın
- Modern web arayüzü
- Görsel sonuçlar

### 3. 🧪 Toplu Test

```bash
python batch_test.py
```

- 10 örnek soru
- Otomatik test

### 4. 🎬 Demo

```bash
python demo.py
```

- Farklı kullanım örnekleri
- Adım adım açıklamalar

### 5. 🔍 Sadece Arama

```bash
python test_search.py
```

- LLM olmadan sadece arama
- Hızlı test

## 📝 Örnek Sorular

### 🏛️ Tarihsel Sorular

- "Mustafa Kemal Atatürk kimdir?"
- "TBMM ne zaman kuruldu?"
- "Kurtuluş Savaşı nasıl başladı?"

### 🎯 Spesifik Konular

- "İzmir'in işgali nasıl gerçekleşti?"
- "Milli Mücadele'nin amacı neydi?"
- "Ankara hangi durumda bulunuyordu?"

### 📊 Analitik Sorular

- "Nutuk'ta hangi konular ele alınır?"
- "En önemli olaylar nelerdir?"
- "Hangi kişilerden bahsedilir?"

## ⚙️ Konfigürasyon

### Model Değiştirme

```python
# rag_system.py içinde
rag = NutukRAGSystem(model_name="llama3:latest")
```

### Arama Sonuç Sayısı

```python
# Daha fazla belge için
rag.ask("soru", k=5)  # Varsayılan k=3
```

### Embedding Modeli

```python
# Farklı embedding modeli
embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
```

## 🔧 Sorun Giderme

### Ollama Çalışmıyor

```bash
# Ollama durumunu kontrol et
ollama list

# Servisi yeniden başlat
ollama serve
```

### ChromaDB Hatası

```bash
# Veritabanını yeniden oluştur
rm -rf rag_chroma_db/
python main.py  # PDF'i tekrar işle
```

### Memory Hatası

```bash
# Daha küçük model kullan
ollama pull phi3:mini
```

### Port Hatası (Web)

```python
# web_app.py içinde portu değiştir
uvicorn.run(app, host="0.0.0.0", port=8080)
```

## 📊 Performans İpuçları

### 🚀 Hızlandırma

- Daha küçük model kullanın (`phi3:mini`)
- Arama sonuç sayısını azaltın (`k=2`)
- GPU kullanın (varsa)

### 🎯 Kalite Artırma

- Daha büyük model kullanın (`llama3:70b`)
- Arama sonuç sayısını artırın (`k=5`)
- Daha iyi embedding modeli seçin

### 💾 Bellek Yönetimi

- Bir seferde az soru sorun
- Modeli düzenli yeniden başlatın
- Sistem kaynaklarını izleyin

## 🆘 Yardım

### Hata Durumunda

1. 🔍 Terminal çıktısını kontrol edin
2. 🔧 Ollama servisini kontrol edin
3. 📚 Bu kılavuzu tekrar okuyun
4. 🆘 GitHub issues'da sorun açın

### Özellik İstekleri

- RAG sistemini geliştirmek isterseniz
- Yeni modeller eklemek isterseniz
- Farklı belgeler işlemek isterseniz

## 🎉 Başarılı Kullanım!

Sistem çalışıyorsa:

- ✅ Embedding modeli yüklendi
- ✅ ChromaDB yüklendi
- ✅ Ollama modeli yüklendi
- ✅ RAG sistemi hazır!

**🎯 Artık Nutuk hakkında istediğiniz soruları sorabilirsiniz!**

---

## 🔗 Faydalı Bağlantılar

- [Ollama](https://ollama.ai) - LLM çalıştırma
- [LangChain](https://langchain.com) - RAG framework
- [ChromaDB](https://chromadb.com) - Vektör veritabanı
- [FastAPI](https://fastapi.tiangolo.com) - Web API

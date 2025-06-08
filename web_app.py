#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from rag_system import NutukRAGSystem
import os

# FastAPI uygulaması
app = FastAPI(title="Nutuk RAG Sistemi", description="Atatürk'ün Nutuk'u üzerinde AI destekli soru-cevap sistemi")

# Templates klasörünü oluştur
templates_dir = "templates"
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)

# Templates'i ayarla
templates = Jinja2Templates(directory=templates_dir)

# RAG sistemini global olarak yükle
print("🚀 RAG sistemi web arayüzü için yükleniyor...")
rag_system = None

@app.on_event("startup")
async def startup_event():
    global rag_system
    rag_system = NutukRAGSystem()
    print("✅ RAG sistemi web arayüzü için hazır!")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Ana sayfa"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Nutuk RAG Sistemi"
    })

@app.post("/ask", response_class=HTMLResponse)
async def ask_question(request: Request, question: str = Form(...)):
    """Soru sor ve yanıt al"""
    global rag_system
    
    if not rag_system:
        error_msg = "RAG sistemi henüz yüklenmedi. Lütfen bekleyin."
        return templates.TemplateResponse("index.html", {
            "request": request,
            "title": "Nutuk RAG Sistemi",
            "error": error_msg
        })
    
    try:
        # Soruyu sor
        print(f"🔍 Web'den gelen soru: {question}")
        
        # İlgili belgeleri bul
        context_docs = rag_system.search_documents(question, k=3)
        
        if not context_docs:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "title": "Nutuk RAG Sistemi",
                "question": question,
                "answer": "İlgili belge bulunamadı.",
                "documents": []
            })
        
        # Yanıt üret
        answer = rag_system.generate_answer(question, context_docs)
        
        # Belge bilgilerini hazırla
        documents_info = []
        for doc in context_docs:
            documents_info.append({
                "page": doc.metadata.get('page', 'Bilinmiyor'),
                "content": doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
            })
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "title": "Nutuk RAG Sistemi",
            "question": question,
            "answer": answer,
            "documents": documents_info
        })
        
    except Exception as e:
        print(f"❌ Web hatası: {e}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "title": "Nutuk RAG Sistemi",
            "question": question,
            "error": f"Hata oluştu: {str(e)}"
        })

@app.get("/health")
async def health_check():
    """Sistem durumu kontrolü"""
    global rag_system
    return {
        "status": "ok" if rag_system else "loading",
        "message": "RAG sistemi hazır" if rag_system else "RAG sistemi yükleniyor"
    }

if __name__ == "__main__":
    print("🌐 Web sunucusu başlatılıyor...")
    print("📍 http://localhost:8000 adresinden erişebilirsiniz")
    uvicorn.run(app, host="0.0.0.0", port=8000)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from improved_rag_system import ImprovedNutukRAGSystem
import os
import time

# FastAPI uygulaması
app = FastAPI(title="İyileştirilmiş Nutuk RAG Sistemi", description="Atatürk'ün Nutuk'u üzerinde gelişmiş AI destekli soru-cevap sistemi")

# Templates klasörünü oluştur
templates_dir = "templates"
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)

# Templates'i ayarla
templates = Jinja2Templates(directory=templates_dir)

# RAG sistemini global olarak yükle
print("🚀 İyileştirilmiş RAG sistemi web arayüzü için yükleniyor...")
rag_system = None

@app.on_event("startup")
async def startup_event():
    global rag_system
    rag_system = ImprovedNutukRAGSystem()
    print("✅ İyileştirilmiş RAG sistemi web arayüzü için hazır!")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Ana sayfa"""
    return templates.TemplateResponse("improved_index.html", {
        "request": request,
        "title": "İyileştirilmiş Nutuk RAG Sistemi"
    })

@app.post("/ask", response_class=JSONResponse)
async def ask_question(request: Request, question: str = Form(...)):
    """Soru sor ve yanıt al"""
    global rag_system
    
    if not rag_system:
        return JSONResponse({
            "success": False,
            "error": "RAG sistemi henüz yüklenmedi. Lütfen bekleyin."
        })
    
    if not question or not question.strip():
        return JSONResponse({
            "success": False,
            "error": "Lütfen bir soru yazın."
        })
    
    try:
        start_time = time.time()
        
        # Soruyu yanıtla
        context_docs = rag_system.search_documents(question, k=6)
        answer = rag_system.generate_answer(question, context_docs)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Kaynak belgeleri hazırla
        sources = []
        for i, doc in enumerate(context_docs, 1):
            sources.append({
                "index": i,
                "page": doc.metadata.get('page', '?'),
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            })
        
        return JSONResponse({
            "success": True,
            "question": question,
            "answer": answer,
            "sources": sources,
            "duration": round(duration, 2),
            "source_count": len(sources)
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": f"Bir hata oluştu: {str(e)}"
        })

@app.get("/health")
async def health_check():
    """Sistem durumu kontrolü"""
    global rag_system
    
    return JSONResponse({
        "status": "healthy" if rag_system else "loading",
        "system_ready": rag_system is not None
    })

@app.get("/api/search/{query}")
async def api_search(query: str, k: int = 6):
    """API endpoint for search only"""
    global rag_system
    
    if not rag_system:
        return JSONResponse({
            "success": False,
            "error": "RAG sistemi henüz yüklenmedi."
        })
    
    try:
        start_time = time.time()
        
        # Sadece arama yap
        context_docs = rag_system.search_documents(query, k=k)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Sonuçları hazırla
        results = []
        for i, doc in enumerate(context_docs, 1):
            results.append({
                "index": i,
                "page": doc.metadata.get('page', '?'),
                "content": doc.page_content,
                "preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            })
        
        return JSONResponse({
            "success": True,
            "query": query,
            "results": results,
            "duration": round(duration, 2),
            "result_count": len(results)
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": f"Arama hatası: {str(e)}"
        })

if __name__ == "__main__":
    print("🌐 İyileştirilmiş Nutuk RAG Web Arayüzü başlatılıyor...")
    print("🔗 http://localhost:8080 adresinde açılacak")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8080,
        log_level="info"
    )

# Nutuk RAG System - Advanced AI-Powered Q&A

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-orange.svg)](https://langchain.com/)

## 🎯 What Does It Do?

This system provides an intelligent Q&A service over Atatürk's **Nutuk** (The Great Speech) using advanced **RAG (Retrieval-Augmented Generation)** technology.

### 🚀 Key Features

- 📚 **Smart Document Processing**: Creates vector database from Nutuk PDF
- 🔍 **Hybrid Search**: Combines semantic and keyword search (BM25)
- 🤖 **AI-Powered Answers**: Uses Ollama for intelligent responses
- 📄 **Source Attribution**: Shows exact page references
- ⚡ **Optimized Performance**: 300-character chunks for better accuracy
- 🌐 **Modern Web UI**: Beautiful, responsive interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai) installed and running

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/SerdarYildiz06/nutuk-rag.git
cd nutuk-rag
```

2. **Create virtual environment**

```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Download Ollama model**

```bash
# Download Qwen2 model (4.4GB)
ollama pull qwen2

# Alternative models:
# ollama pull llama3
# ollama pull mistral
```

5. **Run the improved system**

```bash
# Web interface (recommended)
python improved_web_app.py
# Open http://localhost:8080

# Command line interface
python safe_interactive.py
```

## 📁 Project Structure

```
nutuk-rag/
├── improved_rag_system.py    # 🚀 Enhanced RAG system
├── improved_web_app.py       # 🌐 Modern web interface
├── safe_interactive.py       # 💬 Safe terminal interface
├── rag_system.py            # 📟 Original RAG system
├── web_app.py               # 🌐 Original web interface
├── compare_systems.py       # 🆚 System comparison
├── nutuk.pdf                # 📚 Source document
├── improved_rag_chroma_db/  # 🗃️ Enhanced vector database
├── rag_chroma_db/          # 🗃️ Original vector database
└── templates/              # 🎨 Web templates
```

## 🎮 Usage Options

### 1. 🌐 Web Interface (Recommended)

```bash
python improved_web_app.py
```

- Open http://localhost:8080
- Modern, responsive UI
- Real-time responses
- Source document display

### 2. 💬 Terminal Interface

```bash
python safe_interactive.py
```

- Interactive Q&A
- Type question number or 'q' to quit
- Safe input handling

### 3. 🧪 Quick Demo

```bash
python safe_interactive.py demo
```

- Automated testing
- Example questions
- Performance metrics

### 4. 🆚 System Comparison

```bash
python compare_systems.py
```

- Compare original vs improved system
- Performance benchmarks
- Accuracy tests

## 📝 Example Questions

### 🏛️ Historical Questions

- "Who is Mustafa Kemal Atatürk?"
- "When was the Grand National Assembly established?"
- "How did the War of Independence begin?"

### 🎯 Specific Topics

- "How did the occupation of İzmir occur?"
- "What was the purpose of the National Struggle?"
- "What was Ankara's situation?"

### 📊 Analytical Questions

- "What topics are covered in Nutuk?"
- "What are the most important events?"
- "Which people are mentioned?"

## ⚙️ Configuration

### Change Model

```python
# In improved_rag_system.py
rag = ImprovedNutukRAGSystem(model_name="llama3:latest")
```

### Adjust Search Results

```python
# Get more documents
rag.ask("question", k=8)  # Default k=6
```

### Change Embedding Model

```python
# In improved_rag_system.py
embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
```

## 🚀 Enhanced System Features

### 🔧 New Capabilities

```bash
# Run enhanced system
python improved_rag_system.py

# Enhanced web interface
python improved_web_app.py
# Open http://localhost:8080

# Quick test
python safe_interactive.py demo
```

### ✨ Improvements

- 🔍 **Hybrid Search**: Semantic + Keyword (BM25)
- 📏 **Smaller Chunks**: 300 characters (was: 1000)
- 🧠 **Better Model**: all-mpnet-base-v2
- 🎯 **Reranking**: Smart result ordering
- ⚡ **Faster**: Optimized search
- 🌐 **Modern Web UI**: Enhanced interface

### 🆚 Performance Comparison

| Feature               | Original System | Enhanced System             |
| --------------------- | --------------- | --------------------------- |
| Search Type           | Semantic Only   | Hybrid (Semantic + Keyword) |
| Chunk Size            | 1000 chars      | 300 chars                   |
| Embedding Model       | MiniLM-L12      | MPNet-Base-v2               |
| Reranking             | None            | Advanced                    |
| Accuracy              | Medium          | High                        |
| İzmir Occupation Test | ❌ Fails        | ✅ Finds Page 33            |

## 🔧 Troubleshooting

### Ollama Not Working

```bash
# Check Ollama status
ollama list

# Restart service
ollama serve
```

### ChromaDB Error

```bash
# Rebuild database
rm -rf improved_rag_chroma_db/
python improved_rag_system.py  # Will rebuild automatically
```

### Memory Issues

```bash
# Use smaller model
ollama pull phi3:mini
```

### Port Error (Web)

```python
# Change port in improved_web_app.py
uvicorn.run(app, host="0.0.0.0", port=8081)
```

## 📊 Performance Tips

### 🚀 Speed Optimization

- Use smaller models (`phi3:mini`)
- Reduce search results (`k=3`)
- Use GPU if available

### 🎯 Quality Enhancement

- Use larger models (`llama3:70b`)
- Increase search results (`k=8`)
- Choose better embedding models

### 💾 Memory Management

- Ask fewer questions per session
- Restart model regularly
- Monitor system resources

## 🆘 Support

### Common Issues

1. 🔍 Check terminal output
2. 🔧 Verify Ollama service
3. 📚 Review this guide
4. 🆘 Open GitHub issue

### Feature Requests

- Enhance RAG system
- Add new models
- Process different documents
- Improve multilingual support

## 🎉 Success Indicators

System is working when you see:

- ✅ Embedding model loaded
- ✅ ChromaDB loaded
- ✅ Ollama model loaded
- ✅ RAG system ready!

**🎯 Now you can ask questions about Nutuk!**

## 🏗️ Technical Architecture

### Core Components

- **Document Processing**: PyPDF2 + RecursiveCharacterTextSplitter
- **Vector Store**: ChromaDB with persistent storage
- **Embeddings**: HuggingFace Transformers (all-mpnet-base-v2)
- **Search**: Hybrid (Semantic + BM25 keyword search)
- **LLM**: Ollama (Qwen2, Llama3, Mistral)
- **Web Framework**: FastAPI with Jinja2 templates
- **Reranking**: Custom scoring algorithm

### System Flow

1. 📄 **PDF Processing** → Text extraction and chunking
2. 🔢 **Vectorization** → Create embeddings
3. 🗃️ **Storage** → ChromaDB + BM25 index
4. 🔍 **Search** → Hybrid retrieval
5. 🎯 **Reranking** → Score and sort results
6. 🤖 **Generation** → LLM response with sources

## 🔗 Useful Links

- [Ollama](https://ollama.ai) - Run LLMs locally
- [LangChain](https://langchain.com) - RAG framework
- [ChromaDB](https://chromadb.com) - Vector database
- [FastAPI](https://fastapi.tiangolo.com) - Web API framework
- [HuggingFace](https://huggingface.co) - Transformer models

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=SerdarYildiz06/nutuk-rag&type=Date)](https://star-history.com/#SerdarYildiz06/nutuk-rag&Date)

## 📞 Contact

- 📧 Email: your-email@example.com
- 🐦 Twitter: [@your-twitter](https://twitter.com/your-twitter)
- 💼 LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)

---

**⭐ If you found this project helpful, please give it a star!**

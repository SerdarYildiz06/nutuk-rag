# Gerekli Kütüphaneleri Kurulum
# Bu kütüphaneler bilgisayarınızda yüklü değilse, terminalinizde şu komutları çalıştırın:
# pip install pypdf
# pip install langchain
# pip install sentence-transformers # Gömme modeli için gerekli
# pip install chromadb # ChromaDB için gerekli

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings # Gömme modeli için eklendi
from langchain_community.vectorstores import Chroma # ChromaDB için eklendi

def process_pdf_for_rag(file_path: str):
    """
    Belirtilen PDF dosyasını yükler, metin temizleme uygular ve RAG için parçalara ayırır (chunking).

    Args:
        file_path (str): İşlenecek PDF dosyasının yolu.

    Returns:
        list: Temizlenmiş ve parçalara ayrılmış Document nesnelerinin listesi.
              Bir hata oluşursa None döner.
    """
    if not os.path.exists(file_path):
        print(f"Hata: '{file_path}' yolu bulunamadı. Lütfen dosya yolunu kontrol edin.")
        return None

    print(f"'{file_path}' PDF dosyası yükleniyor ve temizleniyor...")
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load() # Her sayfa ayrı bir 'Document' objesi olarak gelir
    except Exception as e:
        print(f"PDF yükleme sırasında bir hata oluştu: {e}")
        return None

    cleaned_documents = []
    for doc in documents:
        text_content = doc.page_content

        # --- Temel Temizleme Adımları ---
        # 1. Birden fazla boşluğu tek boşluğa indirgeme
        text_content = ' '.join(text_content.split())
        # 2. Yeni satır ve satır başı karakterlerini boşluğa çevirme
        text_content = text_content.replace('\n', ' ').replace('\r', ' ')
        # 3. Baştaki ve sondaki boşlukları kaldırma
        text_content = text_content.strip()

        # Temizlenmiş metinle yeni bir Document objesi oluştur ve metadata'yı kopyala
        cleaned_doc = Document(page_content=text_content, metadata=doc.metadata)
        cleaned_documents.append(cleaned_doc)

    print(f"PDF'den {len(cleaned_documents)} sayfa yüklendi ve temel temizleme yapıldı.")

    if not cleaned_documents:
        print("Uyarı: PDF'den hiç metin çıkarılamadı veya tüm sayfalar boş çıktı.")
        return []

    print("Belgeler parçalara (chunk) ayrılıyor...")
    # --- Chunking (Parçalama) İşlemi ---
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,       # Her parçanın maksimum karakter sayısı
        chunk_overlap=100,     # Parçalar arasındaki çakışan karakter sayısı
        length_function=len,   # Uzunluğu karakter sayısıyla ölç (varsayılan)
        is_separator_regex=False # Ayırıcılar regex mi değil mi? (Varsayılan olarak false bırakın)
    )

    chunks = text_splitter.split_documents(cleaned_documents)
    print(f"Toplam {len(chunks)} parça (chunk) oluşturuldu.")

    return chunks

def create_embeddings_from_chunks(chunks: list[Document]):
    """
    Oluşturulan parçalardan gömme (embedding) vektörleri oluşturur.

    Args:
        chunks (list[Document]): Parçalara ayrılmış Document nesnelerinin listesi.

    Returns:
        HuggingFaceEmbeddings: Yüklenmiş gömme modeli.
        list: Her parça için oluşturulan gömme vektörlerinin listesi.
    """
    print("Gömme modeli yükleniyor ve parçalar vektörlere dönüştürülüyor...")
    # Türkçe için veya genel amaçlı bir model seçin
    embedding_model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    try:
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        print(f"Gömme modeli yüklendi: {embedding_model_name}")

        # Her bir parçanın içeriğinden gömme vektörlerini oluşturma
        # Not: LangChain'in vektör veritabanları genellikle bu adımı otomatik yapar,
        # ancak burada manuel olarak da gösterebiliriz.
        # embedded_chunks = embeddings.embed_documents([chunk.page_content for chunk in chunks])
        # print(f"{len(embedded_chunks)} adet gömme vektörü oluşturuldu.")
        
        # Bu fonksiyon, doğrudan `embeddings` objesini döndürüyor.
        # Vektör veritabanına kaydederken parçalar bu modelle embed edilecek.
        return embeddings
    except Exception as e:
        print(f"Gömme modeli yüklenirken veya gömme oluşturulurken bir hata oluştu: {e}")
        print("Lütfen 'sentence-transformers' kütüphanesinin yüklü olduğundan ve internet bağlantınızın olduğundan emin olun.")
        return None

def save_to_chromadb(chunks: list[Document], embeddings_model, persist_directory: str = "rag_chroma_db"):
    """
    Parçaları ChromaDB vektör veritabanına kaydeder.

    Args:
        chunks (list[Document]): Parçalara ayrılmış Document nesnelerinin listesi.
        embeddings_model: Gömme modeli (HuggingFaceEmbeddings).
        persist_directory (str): ChromaDB'nin kaydedileceği dizin yolu.

    Returns:
        Chroma: ChromaDB vektör mağazası objesi. Hata durumunda None döner.
    """
    if not chunks or not embeddings_model:
        print("Hata: Parçalar veya gömme modeli bulunamadı.")
        return None

    print(f"ChromaDB'ye kaydetme işlemi başlatılıyor...")
    print(f"Kayıt dizini: {persist_directory}")
    print(f"Kaydedilecek parça sayısı: {len(chunks)}")

    try:
        # ChromaDB vektör mağazası oluşturma ve parçaları kaydetme
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings_model,
            persist_directory=persist_directory
        )
        
        print(f"✅ {len(chunks)} parça başarıyla ChromaDB'ye kaydedildi.")
        print(f"📁 Vektör veritabanı şu konumda saklanıyor: {persist_directory}")
        
        # Vektör mağazasındaki toplam doküman sayısını kontrol etme
        collection = vectorstore._collection
        total_docs = collection.count()
        print(f"📊 Vektör veritabanındaki toplam doküman sayısı: {total_docs}")
        
        return vectorstore
        
    except Exception as e:
        print(f"❌ ChromaDB'ye kaydetme sırasında bir hata oluştu: {e}")
        print("Lütfen 'chromadb' kütüphanesinin yüklü olduğundan emin olun.")
        return None

def search_in_vectorstore(vectorstore, query: str, k: int = 5):
    """
    ChromaDB vektör mağazasında arama yapar.

    Args:
        vectorstore: ChromaDB vektör mağazası objesi.
        query (str): Aranacak sorgu metni.
        k (int): Döndürülecek en benzer doküman sayısı.

    Returns:
        list: En benzer dokümanların listesi.
    """
    if not vectorstore:
        print("Hata: Vektör mağazası bulunamadı.")
        return []

    try:
        print(f"🔍 Sorgu: '{query}'")
        print(f"📝 {k} adet en benzer doküman aranıyor...")
        
        # Benzerlik araması yapma
        similar_docs = vectorstore.similarity_search(query, k=k)
        
        print(f"✅ {len(similar_docs)} adet benzer doküman bulundu.")
        
        for i, doc in enumerate(similar_docs):
            print(f"\n--- Sonuç {i+1} ---")
            print(f"Kaynak: {doc.metadata.get('source', 'Bilinmiyor')}")
            print(f"Sayfa: {doc.metadata.get('page', 'Bilinmiyor')}")
            print(f"İçerik: {doc.page_content[:200]}...")
            
        return similar_docs
        
    except Exception as e:
        print(f"❌ Arama sırasında bir hata oluştu: {e}")
        return []

if __name__ == "__main__":
    # --- Kullanıcıdan PDF Dosya Yolu Alma ---
    print("PDF dosya yolunu girin (Örn: C:/Users/KullaniciAdi/Belgelerim/rapor.pdf)")
    pdf_file_path = input("PDF Dosya Yolu: ")

    # PDF'i işleme ve parçaları alma
    processed_chunks = process_pdf_for_rag(pdf_file_path)

    if processed_chunks:
        print("\n--- İşlem Sonuçları ---")
        print(f"İşlenen toplam parça sayısı: {len(processed_chunks)}")

        # İlk birkaç parçanın içeriğini kontrol edelim
        print("\n--- Oluşturulan İlk 3 Parçanın İçeriği ---")
        for i, chunk in enumerate(processed_chunks[:3]):
            print(f"\n--- Parça {i+1} ---")
            print(f"Karakter Sayısı: {len(chunk.page_content)}")
            print(f"Metada (Kaynak Dosya, Sayfa Numarası vb.): {chunk.metadata}")
            print("İçerik Başlangıcı:")
            print(chunk.page_content[:400]) # İlk 400 karakterini göster
            print("...")
        
        # Parçalardan gömme vektörleri oluşturma (Gömme modeli döndürülüyor)
        # Bu fonksiyon aslında embedding modelini döndürür, vektör veritabanı adımında kullanılır
        embeddings_model = create_embeddings_from_chunks(processed_chunks)

        if embeddings_model:
            print("\nParçalardan gömme vektörleri oluşturma aşamasına geçildi.")
            
            # ChromaDB'ye kaydetme işlemi
            print("\n=== ChromaDB'ye Kaydetme İşlemi ===")
            vectorstore = save_to_chromadb(processed_chunks, embeddings_model)
            
            if vectorstore:
                print("\n✅ ChromaDB'ye kaydetme işlemi tamamlandı!")
                
                # Kullanıcıdan arama sorgusu alma
                print("\n=== Arama Testi ===")
                print("ChromaDB'de arama yapmak ister misiniz? (e/h)")
                search_choice = input("Seçiminiz: ").lower()
                
                if search_choice == 'e':
                    while True:
                        query = input("\nArama sorgusu girin (çıkmak için 'quit'): ")
                        if query.lower() == 'quit':
                            break
                        
                        search_results = search_in_vectorstore(vectorstore, query)
                        
                        if not search_results:
                            print("Hiç sonuç bulunamadı.")
                else:
                    print("Arama işlemi atlandı.")
                    
                print("\n📋 Vektör veritabanı kullanımı:")
                print("Daha sonra arama yapmak için:")
                print("vectorstore = Chroma(persist_directory='rag_chroma_db', embedding_function=embeddings_model)")
                print("results = vectorstore.similarity_search('sorgunuz')")
            else:
                print("\n❌ ChromaDB'ye kaydetme işlemi başarısız oldu.")
        else:
            print("\nGömme modeli oluşturulamadı. Lütfen hataları kontrol edin.")

    else:
        print("\nPDF işleme sırasında bir sorun oluştu, parçalar oluşturulamadı.")

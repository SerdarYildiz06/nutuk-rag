#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

def manual_izmir_test():
    """İzmir işgali hakkında manuel test"""
    
    # Sayfa 33'teki tam içerik
    sayfa_33_icerik = """
Cemiyeti vardı. Bu cemiyet merkezinin gönder­ diği delegelerle, Of kazasıyla Lazistan livası dahilinde şubeler açılmıştı (Ve­ sika: 5, 6). İzmir'in işgal olunacağına dair Mayıs'ın on üçünden beri fiili emareler gö­ ren İzmir'de bazı genç vatanperverler, ayın 14/15'inci gecesi, bu acı vaziyet hakkında fikir alışverişinde bulunmuşlar ve emrivaki haline geldiğine şüphe kalmayan Yunan işgalinin ilhakla neticelenmesine mani olmak esasında müt­ tefik kalmışlar ve Reddi İlhak prensibini ortaya atmışlardır. Aynı gecede bu maksadın yayılmasını temin için İzmir'de Yahudi mezarlığında toplanabilen halk tarafından bir miting yapılmışsa da, ertesi gün sabahleyin Yunan asker­ lerinin rıhtımda görülmesiyle bu teşebbüs ümit edilen derecede maksadı te­ min edememiştir.
"""
    
    # LLM'i başlat
    llm = OllamaLLM(model="qwen2:latest")
    
    # İyileştirilmiş prompt
    prompt_template = ChatPromptTemplate.from_template("""
Sen Atatürk'ün Nutuk eseri konusunda uzman bir tarihçisin. Aşağıdaki belgeler kullanılarak soruyu detaylı ve açık bir şekilde yanıtla. 

Önemli kurallar:
- Belgelerde açık bir bilgi varsa, o bilgiyi tam olarak kullan
- Tarihleri, isimleri ve olayları olduğu gibi aktar
- Eğer belgelerden tam yanıt bulamıyorsan, "Bu konuda belgede yeterli bilgi bulunmuyor" de
- Hangi sayfalardan bilgi aldığını belirt

Belgeler:
Sayfa 33: {context}

Soru: {question}

Yanıt: Verilen belgelere dayanarak,""")
    
    # Soruyu sor
    question = "İzmir'in işgali nasıl gerçekleşti?"
    
    formatted_prompt = prompt_template.format(
        context=sayfa_33_icerik,
        question=question
    )
    
    print("🤖 Ollama ile yanıt üretiliyor...")
    print(f"📄 Kullanılan belge: Sayfa 33")
    print(f"❓ Soru: {question}")
    print("="*60)
    
    response = llm.invoke(formatted_prompt)
    print(f"💬 Yanıt:\n{response}")
    print("="*60)

if __name__ == "__main__":
    manual_izmir_test()

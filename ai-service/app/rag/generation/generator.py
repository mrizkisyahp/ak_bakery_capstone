from openai import OpenAI

from app.core.config import get_settings

class ResponseGenerator:
  
  def __init__(self):
    settings = get_settings()
    
    self.client = OpenAI(
      api_key=settings.gonka_api_key.get_secret_value(),
      base_url=settings.gonka_base_url,
    )
    
    self.model = settings.llm_model
  
  def generate(
    self,
    message: str,
    context: list[dict],
    prompt_type: str
  ) -> str:
    if not message or not message.strip():
      raise ValueError("Message cannot be empty")
    
    if not context:
      raise ValueError("Context cannot be empty")
    
    system_prompt = self._build_system_prompt(prompt_type)
    faq_context = self._format_context(context)
    
    response = self.client.chat.completions.create(
      model=self.model,
      messages=[
        {
          "role": "system",
          "content": system_prompt,
        },
        {
          "role": "user",
          "content": (
            f"Informasi FAQ Adiskirani Bakery:\n"
            f"{faq_context}\n\n"
            f"Pertanyaan pengguna:\n{message}"
          ),
        },
      ],
      max_tokens=1024
    )
    
    answer = response.choices[0].message.content
    
    if not answer or not answer.strip():
      raise RuntimeError("LLM returned an empty response")
    
    return answer.strip()

  @staticmethod
  def _format_context(context: list[dict]) -> str:
    formatted_context = []
    
    for index, item in enumerate(context, start=1):
      formatted_context.append(
        f"FAQ {index}:\n"
        f"Pertanyaan: {item['question']}\n"
        f"Jawaban: {item['answer']}"
      )
    
    return "\n\n".join(formatted_context)

  @staticmethod
  def _build_system_prompt(prompt_type:str) -> str:
    prompt_templates = {
      "product_inquiry": (
        "Kamu adalah asisten virtual Adiskirani Bakery. "
        "Jawab pertanyaan tentang produk berdasarkan konteks FAQ. "
        "Jangan mengarang informasi yang tidak tersedia."
      ),
      "ordering": (
        "Kamu adalah asisten virtual Adiskirani Bakery. "
        "Bantu pengguna memahami informasi pemesanan berdasarkan "
        "konteks FAQ. Jangan mengarang prosedur pemesanan. "
        "Arahkan pengguna untuk mengubungi Adiskirani Bakery "
        "melalui WhatsApp jika ingin melakukan pesanan."
      ),
      "complaint": (
        "Kamu adalah asisten virtual Adiskirani Bakery. "
        "Tanggapi keluhan pengguna dengan sopan dan empatik. "
        "Gunakan konteks FAQ jika relevan dan jangan menjanjikan "
        "penyelesaian yang tidak tercantum di dalamnya. "
        "Arahkan pengguna untuk menyampaikan keluhannya "
        "lebih lenjut melalui WhatsApp Adiskirani Bakery."
      ),
      "other": (
        "Kamu adalah asisten virtual Adiskirani Bakery. "
        "Jawab pertanyaan hanya jika masih relevan dengan "
        "informasi bisnis Adiskirani Bakery dalam konteks FAQ."
        "Jika di luar cakupan, sampaikan dengan sopan."
      )
    }
    
    if prompt_type not in prompt_templates:
      raise ValueError(
        f"Unsupported prompt type: {prompt_type}"
      )
      
    return (
      prompt_templates[prompt_type]
      + "\n\n"
      + "Gunakan hanya informasi dalam konteks FAQ sebagai "
      "sumber fakta. Jika informasi tidak cukup untuk menjawab, "
      "jelaskan keterbatasan informasi tersebut. "
      "Jangan membuat asumsi atau informasi baru. "
      "Jangan mengarang nomor WhatsApp atau tautan kontak."
    )
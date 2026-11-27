from app.intent.schemas import IntentRoutingResult
from app.rag.retrieval.retriever import FAQRetriever
from app.rag.generation.generator import ResponseGenerator

class RAGPipeline:
  
  FALLBACK_RESPONSE = (
    "Maaf, informasi tersebut belum tersedia dalam "
    "basis pengetahuan chatbot Adiskirani Bakery. "
    "Silakan hubungi pihak Adiskirani Bakery untuk "
    "mendapatkan informasi lebih lanjut."
  )
  
  def __init__(
    self,
    retriever: FAQRetriever | None = None,
    generator: ResponseGenerator | None = None
  ):
    self.retriever = retriever or FAQRetriever()
    self.generator = generator or ResponseGenerator()
    
  def run(
    self,
    message: str,
    routing_result: IntentRoutingResult,
  ) -> str:
    if not message or not message.strip():
      raise ValueError("Message cannot be empty")
    
    if not isinstance(routing_result, IntentRoutingResult):
      raise TypeError(
        "routing_result must be an IntentRoutingResult"
      )
      
    # retrieve relevant FAQ context
    retrieved_context = self.retriever.retrieve(message)
    
    # return fallback if no relevant FAQ is found
    if not retrieved_context:
      return self.FALLBACK_RESPONSE

    # generate an answer based on retrieved FAQ context
    answer = self.generator.generate(
      message=message,
      context=retrieved_context,
      prompt_type=routing_result.prompt_type,
    )
    
    return answer
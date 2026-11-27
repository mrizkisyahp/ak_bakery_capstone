from typing import TYPE_CHECKING

from app.intent.classifier import DummyIntentClassifier
from app.intent.router import IntentRouter
from app.schemas.chat import ChatResponse

if TYPE_CHECKING:
  from app.rag.pipeline import RAGPipeline

class ChatService:
  
  def __init__(
    self,
    rag_pipeline: "RAGPipeline",
    classifier: DummyIntentClassifier | None = None,
    router: IntentRouter | None = None,
  ):
    self.classifier = classifier or DummyIntentClassifier()
    self.router = router or IntentRouter()
    self.rag_pipeline = rag_pipeline
  
  def process_message(self, message: str) -> ChatResponse:
    
    if not message or not message.strip():
      raise ValueError("Message cannot be empty")
    
    # classify user intent
    classification = self.classifier.classify(message)
    
    # determine routing and prompt type
    routing_result = self.router.route(classification)
    
    # process message through RAG pipeline
    answer = self.rag_pipeline.run(
      message=message,
      routing_result=routing_result
    )
    
    # return chatbot response
    return ChatResponse(answer=answer)
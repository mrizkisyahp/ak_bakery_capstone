import unittest
from unittest.mock import Mock

from app.intent.schemas import IntentRoutingResult
from app.rag.pipeline import RAGPipeline

class TestRAGPipeline(unittest.TestCase):
  
  def setUp(self):
    self.retriever = Mock()
    self.generator = Mock()
    
    self.pipeline = RAGPipeline(
      retriever=self.retriever,
      generator=self.generator
    )
    
    self.routing_result = IntentRoutingResult(
      intent="product_inquiry",
      prompt_type="product_inquiry",
      confidence=0.95,
      fallback_applied=False
    )
    
  def test_run_success(self):
    context = [
      {
        "question": "Apa produk Adiskirani Bakery?",
        "answer": "Produk bakery.",
        "score": 0.90
      }
    ]
    
    self.retriever.retrieve.return_value = context
    self.generator.generate.return_value = (
      "Adiskirani menjual produk bakery."
    )
    
    result = self.pipeline.run(
      message="Apa produk Adiskirani Bakery?",
      routing_result=self.routing_result
    )
    
    self.assertEqual(
      result,
      "Adiskirani menjual produk bakery."
    )
    
    self.retriever.retrieve.assert_called_once_with(
      "Apa produk Adiskirani Bakery?"
    )
    
    self.generator.generate.assert_called_once_with(
      message="Apa produk Adiskirani Bakery?",
      context=context,
      prompt_type="product_inquiry"
    )
    
  def test_run_returns_fallback_when_no_context(self):
    self.retriever.retrieve.return_value = []
    
    result = self.pipeline.run(
      message="Apa produk Adiskirani Bakery?",
      routing_result=self.routing_result 
    )
    
    self.assertEqual(
      result,
      self.pipeline.FALLBACK_RESPONSE,
    )
    
    self.generator.generate.assert_not_called()
  
  def test_run_empty_message_raises_error(self):
    with self.assertRaises(ValueError):
      self.pipeline.run(
        message="",
        routing_result=self.routing_result,
      )
    
    self.retriever.retrieve.assert_not_called()
    self.generator.generate.assert_not_called()
    
  def test_run_invalid_routing_result_raises_error(self):
    with self.assertRaises(TypeError):
      self.pipeline.run(
        message="Apa produk Adiskirani Bakery?",
        routing_result={"intent": "product_inquiry"},
      )
      
    self.retriever.retrieve.assert_not_called()
    self.generator.generate.assert_not_called()
    
if __name__ == "__main__":
  unittest.main()
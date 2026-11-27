import unittest
from unittest.mock import Mock

from app.schemas.chat import ChatResponse
from app.services.chat_service import ChatService

class TestChatService(unittest.TestCase):
  
  def setUp(self):
    self.classifier = Mock()
    self.router = Mock()
    self.rag_pipeline = Mock()
    
    self.chat_service = ChatService(
      rag_pipeline=self.rag_pipeline,
      classifier=self.classifier,
      router=self.router,
    )
    
    self.message = "Apa produk Adiskirani Bakery?"
    
    self.classification = Mock()
    self.routing_result = Mock()
    
    self.classifier.classify.return_value = self.classification
    self.router.route.return_value = self.routing_result
    self.rag_pipeline.run.return_value = (
      "Adiskirani menjual produk bakery."
    )
    
  def test_process_message_success(self):
    result = self.chat_service.process_message(
      self.message
    )
    
    self.assertIsInstance(result, ChatResponse)
    self.assertEqual(
      result.answer,
      "Adiskirani menjual produk bakery."
    )
    
    self.classifier.classify.assert_called_once_with(
      self.message
    )
    
    self.router.route.assert_called_once_with(
      self.classification
    )
    
    self.rag_pipeline.run.assert_called_once_with(
      message=self.message,
      routing_result=self.routing_result,
    )
    
  def test_process_message_empty_raises_error(self):
    with self.assertRaises(ValueError):
      self.chat_service.process_message("   ")
    
    self.classifier.classify.assert_not_called()
    self.router.route.assert_not_called()
    self.rag_pipeline.run.assert_not_called()
    
  def test_process_message_whitespace_raises_error(self):
    with self.assertRaises(ValueError):
      self.chat_service.process_message("  ")
      
      self.classifier.classify.assert_not_called()
      self.router.route.assert_not_called()
      self.rag_pipeline.run.assert_not_called()
    
  def test_classifier_error_is_propagated(self):
    self.classifier.classify.side_effect = RuntimeError(
      "Classifier error"
    )
    
    with self.assertRaisesRegex(
      RuntimeError,
      "Classifier error",
    ):
      self.chat_service.process_message(
        self.message
      )

    self.router.route.assert_not_called()
    self.rag_pipeline.run.assert_not_called()
    
  def test_router_error_is_propagated(self):
    self.router.route.side_effect = RuntimeError(
      "Router error"
    )
    
    with self.assertRaisesRegex(
      RuntimeError,
      "Router error"
    ):
      self.chat_service.process_message(
        self.message
      )
      
      self.classifier.classify.assert_called_once_with(
        self.message
      )
      self.rag_pipeline.run.assert_not_called()
    
  def test_rag_pipeline_error_is_propagated(self):
    self.rag_pipeline.run.side_effect = RuntimeError(
      "RAG Pipeline error"
    )
    
    with self.assertRaisesRegex(
      RuntimeError,
      "RAG Pipeline error"
    ):
      self.chat_service.process_message(
        self.message
      )
    
    self.classifier.classify.assert_called_once_with(
      self.message
    )
    
    self.router.route.assert_called_once_with(
      self.classification
    )
    
if __name__ == "__main__":
  unittest.main()
import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace

from app.rag.embeddings.embedding_service import EmbeddingService

class TestEmbeddingService(unittest.TestCase):
  
  def setUp(self):
    self.embedding_client = Mock()
    
    self.settings_patcher = patch(
      "app.rag.embeddings.embedding_service.get_settings",
      return_value=SimpleNamespace(
        embedding_dimension=3
      ),
    )
    self.settings_patcher.start()
    
    self.addCleanup(self.settings_patcher.stop)
    
    self.embedding_service = EmbeddingService(
      embedding_client=self.embedding_client
    )
    
  def test_embed_success(self):
    expected_vector = [0.1, 0.2, 0.3]
    
    self.embedding_client.create_embedding.return_value = (
      expected_vector
    )
    
    result = self.embedding_service.embed("Apa produk Adiskirani Bakery?")
    
    self.assertEqual(result, expected_vector)
    self.embedding_client.create_embedding.assert_called_once_with(
      "Apa produk Adiskirani Bakery?"
    )
    
  def test_embed_empty_text_raises_error(self):
    with self.assertRaises(ValueError):
      self.embedding_service.embed("")
    
    self.embedding_client.create_embedding.assert_not_called()
    
  def test_embed_whitespace_text_raises_error(self):
    with self.assertRaises(ValueError):
      self.embedding_service.embed("    ")
      
    self.embedding_client.create_embedding.assert_not_called()
  
  def test_embed_invalid_dimension_raises_error(self):
    invalid_vector = [0.1, 0.2]
    
    self.embedding_client.create_embedding.return_value = (
      invalid_vector
    )
    
    with self.assertRaisesRegex(
      ValueError,
      "Invalid embedding dimension",
    ):
      self.embedding_service.embed("Apa produk Adiskirani Bakery?")

if __name__ == "__main__":
  unittest.main()
    
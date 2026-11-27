import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from app.rag.retrieval.retriever import FAQRetriever

class TestFAQRetriever(unittest.TestCase):
  
  def setUp(self):
    self.embedding_service = Mock()
    self.embedding_service.embed.return_value = [0.1, 0.2, 0.3]
    
    self.qdrant_client = Mock()
    
    self.qdrant_connection = Mock()
    self.qdrant_connection.get_client.return_value = (
      self.qdrant_client
    )
    self.qdrant_connection.collection_name = "adiskirani_faq"
    
    self.retriever = FAQRetriever(
      embedding_service=self.embedding_service,
      qdrant_connection=self.qdrant_connection
    )
    
  def test_retrieve_success(self):
    self.qdrant_client.query_points.return_value = (
      SimpleNamespace(
        points=[
          SimpleNamespace(
            score=0.85,
            payload={
              "question": "Apa produk Adiskirani Bakery?",
              "answer": "Adiskirani menjual berbagai produk bakery.",
              "is_active": True
            },
          )
        ]
      )
    )
    
    result = self.retriever.retrieve("Apa produk Adiskirani Bakery?")
    
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0]["score"], 0.85)
    
    self.embedding_service.embed.assert_called_once_with(
      "Apa produk Adiskirani Bakery?"
    )
    self.qdrant_client.query_points.assert_called_once()
    
  def test_retrieve_ignores_low_score(self):
    self.qdrant_client.query_points.return_value = (
      SimpleNamespace(
        points=[
          SimpleNamespace(
            score=0.50,
            payload={
              "question": "Apa produl Adiskirani Bakery?",
              "answer": "Informasi produk."
            }
          )
        ]
      )
    )
    
    result = self.retriever.retrieve("Pertanyaan pengguna")
    self.assertEqual(result, [])
    
  def test_retrieve_ignores_incomplete_payload(self):
    self.qdrant_client.query_points.return_value = (
      SimpleNamespace(
        points=[
          SimpleNamespace(
            score=0.90,
            payload={
              "question": "Apa produk Adiskirani Bakery?",
            }
          )
        ]
      )
    )
    
    result = self.retriever.retrieve("Pertanyaan pengguna")
    
    self.assertEqual(result, [])
    
  def test_retrieve_empty_result(self):
    self.qdrant_client.query_points.return_value = (
      SimpleNamespace(points=[])
    )
    
    result = self.retriever.retrieve("Pertanyaan pengguna")
    
    self.assertEqual(result, [])
    
  def test_retrieve_empty_query_raises_error(self):
    with self.assertRaises(ValueError):
      self.retriever.retrieve("")
      
    self.embedding_service.embed.assert_not_called()
    self.qdrant_client.query_points.assert_not_called()
    
  def test_retrieve_uses_active_faq_filter(self):
    self.qdrant_client.query_points.return_value = (
      SimpleNamespace(points=[])
    )
    
    self.retriever.retrieve("Pertanyaan pengguna")
    
    call_arguments = (
      self.qdrant_client.query_points.call_args.kwargs
    )
    
    self.assertEqual(
      call_arguments["collection_name"],
      "adiskirani_faq"
    )
    self.assertEqual(call_arguments["limit"], 5)
    self.assertTrue(call_arguments["with_payload"])
    
    query_filter = call_arguments["query_filter"]
    
    self.assertEqual(len(query_filter.must), 1)
    self.assertEqual(
      query_filter.must[0].key,
      "is_active",
    )
    self.assertTrue(
      query_filter.must[0].match.value
    )
    
if __name__ == "__main__":
  unittest.main()
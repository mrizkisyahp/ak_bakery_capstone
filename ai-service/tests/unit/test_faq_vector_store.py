import unittest
from unittest.mock import MagicMock

from app.rag.storage.faq_vector_store import FAQVectorStore

class TestFAQVectorStore(unittest.TestCase):
  
  def setUp(self):
    self.mock_client = MagicMock()
    
    self.mock_connection = MagicMock()
    self.mock_connection.get_client.return_value = self.mock_client
    self.mock_connection.collection_name = "adiskirani_faq"
    
    self.vector_store = FAQVectorStore(
      qdrant_connection=self.mock_connection
    )
    
    self.embedding = [0.1, 0.2, 0.3]
    
  def test_upsert_faq_success(self):
    self.vector_store.upsert_faq(
      faq_id=1,
      question="Bagaimana cara memesan?",
      answer="Hubungi Adiskirani melalui WhatsApp.",
      embedding=self.embedding
    )
    
    self.mock_client.upsert.assert_called_once()
    
    call_kwargs = self.mock_client.upsert.call_args.kwargs
    point = call_kwargs["points"][0]
    
    self.assertEqual(point.id, 1)
    self.assertEqual(point.vector, self.embedding)
    self.assertEqual(
      point.payload["question"],
      "Bagaimana cara memesan?",
    )
    self.assertEqual(
      point.payload["answer"],
      "Hubungi Adiskirani melalui WhatsApp."
    )
    self.assertTrue(point.payload["is_active"])
    
    self.assertEqual(
      call_kwargs["collection_name"],
      "adiskirani_faq"
    )
    self.assertTrue(call_kwargs["wait"])
    
  def test_upsert_faq_inactive(self):
    self.vector_store.upsert_faq(
      faq_id=1,
      question="Bagaimana cara memesan?",
      answer="Hubungi Adiskirani melalui WhatsApp.",
      embedding=self.embedding,
      is_active=False
    )
    
    call_kwargs = self.mock_client.upsert.call_args.kwargs
    point = call_kwargs["points"][0]
    
    self.assertFalse(point.payload["is_active"])
  
  def test_upsert_same_faq_id(self):
    for answer in ["Jawaban pertama", "Jawaban terbaru"]:
      self.vector_store.upsert_faq(
        faq_id=1,
        question="Bagaimana cara memesan?",
        answer=answer,
        embedding=self.embedding
      )
      
    self.assertEqual(self.mock_client.upsert.call_count, 2)
    
    first_point = (
      self.mock_client.upsert.call_args_list[0]
      .kwargs["points"][0]
    )
    
    second_point = (
      self.mock_client.upsert.call_args_list[1]
      .kwargs["points"][0]
    )
    
    self.assertEqual(first_point.id, second_point.id)
  
  def test_upsert_invalid_faq_id(self):
    with self.assertRaises(ValueError):
      self.vector_store.upsert_faq(
        faq_id=0,
        question="Pertanyaan",
        answer="Jawaban",
        embedding=self.embedding
      )
    
    self.mock_client.upsert.assert_not_called()
  
  def test_upsert_empty_question(self):
    with self.assertRaises(ValueError):
      self.vector_store.upsert_faq(
        faq_id=1,
        question=" ",
        answer="Jawaban",
        embedding=self.embedding
      )
    
    self.mock_client.upsert.assert_not_called()
  
  def test_upsert_empty_answer(self):
    with self.assertRaises(ValueError):
      self.vector_store.upsert_faq(
        faq_id=1,
        question="Pertanyaan",
        answer=" ",
        embedding=self.embedding
      )
    
    self.mock_client.upsert.assert_not_called()

  def test_upsert_empty_embedding(self):
    with self.assertRaises(ValueError):
      self.vector_store.upsert_faq(
        faq_id=1,
        question="Pertanyaan",
        answer="Jawaban",
        embedding=[]
      )
    
    self.mock_client.upsert.assert_not_called()
  
if __name__ == "__main__":
  unittest.main()
import unittest
from app.intent.classifier import DummyIntentClassifier

class TestDummyIntentClassifier(unittest.TestCase):
  
  def setUp(self):
    self.classifier = DummyIntentClassifier()
  
  def test_product_inquiry(self):
    result = self.classifier.classify("Berapa harga roti tawar?")
    
    self.assertEqual(result.intent, "product_inquiry")
    self.assertEqual(result.confidence, 0.95)
  
  def test_ordering(self):
    result = self.classifier.classify(
      "Saya mau pesan snack box"
    )
    
    self.assertEqual(result.intent, "ordering")
    self.assertEqual(result.confidence, 0.95)
  
  def test_complaint(self):
    result = self.classifier.classify(
      "Pesanan saya terlambat"
    )
    
    self.assertEqual(result.intent, "complaint")
    self.assertEqual(result.confidence, 0.95)
  
  def test_other(self):
    result = self.classifier.classify(
      "Siapa presiden Indonesia?"
    )
    
    self.assertEqual(result.intent, "other")
    self.assertEqual(result.confidence, 0.50)
  
  def test_empty_message(self):
    result = self.classifier.classify(
      ""
    )
    
    self.assertEqual(result.intent, "other")
    self.assertEqual(result.confidence, 0.0)
    
  def test_whitespace_message(self):
      result = self.classifier.classify(
        "          "
      )
      
      self.assertEqual(result.intent, "other")
      self.assertEqual(result.confidence, 0.0)
  
  def test_multiple_matching_intents(self):
      result = self.classifier.classify(
        "Saya mau pesan, tetapi produk yang datang rusak"
      )
      
      self.assertEqual(result.intent, "complaint")
      self.assertEqual(result.confidence, 0.95)
      
if __name__ == "__main__":
  unittest.main()
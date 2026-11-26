import unittest

from pydantic import ValidationError

from app.intent.router import IntentRouter
from app.intent.schemas import (
  IntentClassificationResult,
  IntentRoutingResult
)

class TestIntentRouter(unittest.TestCase):
  
  def setUp(self):
    self.router = IntentRouter()
    
  def test_product_inquiry_routing(self):
    classification = IntentClassificationResult(
      intent="product_inquiry",
      confidence=0.95
    )
    
    result = self.router.route(classification)
    
    self.assertEqual(result.intent, "product_inquiry")
    self.assertEqual(result.prompt_type, "product_inquiry")
    self.assertEqual(result.confidence, 0.95)
    self.assertFalse(result.fallback_applied)
  
  def test_ordering_routing(self):
    classification = IntentClassificationResult(
      intent="ordering",
      confidence=0.90
    )
    
    result = self.router.route(classification)
    
    self.assertEqual(result.prompt_type, "ordering")
    self.assertFalse(result.fallback_applied)
    
  def test_complaint_routing(self):
    classification = IntentClassificationResult(
      intent="complaint",
      confidence=0.90
    )
    
    result = self.router.route(classification)
    
    self.assertEqual(result.prompt_type, "complaint")
    self.assertFalse(result.fallback_applied)
        
  def test_other_routing(self):
    classification = IntentClassificationResult(
      intent="other",
      confidence=0.80
    )
    
    result = self.router.route(classification)
    
    self.assertEqual(result.intent, "other")
    self.assertEqual(result.prompt_type, "other")
    self.assertFalse(result.fallback_applied)
      
  def test_low_confidence_uses_fallback(self):
    classification = IntentClassificationResult(
      intent="product_inquiry",
      confidence=0.42
    )
    
    result = self.router.route(classification)
    
    self.assertEqual(result.intent, "product_inquiry")
    self.assertEqual(result.prompt_type, "other")
    self.assertEqual(result.confidence, 0.42)
    self.assertTrue(result.fallback_applied)
      
  def test_confidence_equal_to_threshold_is_accepted(self):
    classification = IntentClassificationResult(
      intent="product_inquiry",
      confidence=0.70
    )
    
    result = self.router.route(classification)
    
    self.assertEqual(result.intent, "product_inquiry")
    self.assertFalse(result.fallback_applied)
  
  def test_unknown_intent_raises_error(self):
    classification = IntentClassificationResult(
      intent="unknown_intent",
      confidence=0.90
    )
    
    with self.assertRaises(ValueError):
      self.router.route(classification)
  
  def test_invalid_input_type_raises_error(self):
    with self.assertRaises(TypeError):
      self.router.route(
        {
          "intent": "product_inquiry"
        }
      )
  
  def test_invalid_confidence_is_rejected_by_schema(self):
    with self.assertRaises(ValidationError):
      IntentClassificationResult(
        intent="product_inquiry",
        confidence=1.50
      )
      
if __name__ == "__main__":
  unittest.main()
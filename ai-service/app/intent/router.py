from app.intent.schemas import (
  IntentClassificationResult,
  IntentRoutingResult
)

class IntentRouter:
  CONFIDENCE_THRESHOLD = 0.70
  FALLBACK_PROMPT_TYPE = "other"
  
  ROUTING_MAPPING = {
    "product_inquiry": "product_inquiry",
    "ordering": "ordering",
    "complaint": "complaint",
    "other": "other",
  }
  
  def route(
    self,
    classification: IntentClassificationResult,
  ) -> IntentRoutingResult:
    if not isinstance(classification, IntentClassificationResult):
      raise TypeError(
        "classification must be an IntentClassificationResult"
      )
      
    if classification.intent not in self.ROUTING_MAPPING:
      raise ValueError(
        f"Unsupported intent: {classification.intent}"
      )
    
    fallback_applied = (
      classification.confidence < self.CONFIDENCE_THRESHOLD
    )
    
    if fallback_applied:
      prompt_type = self.FALLBACK_PROMPT_TYPE
    else:
      prompt_type = self.ROUTING_MAPPING[classification.intent]
      
    return IntentRoutingResult(
      intent=classification.intent,
      prompt_type=prompt_type,
      confidence=classification.confidence,
      fallback_applied=fallback_applied
    )
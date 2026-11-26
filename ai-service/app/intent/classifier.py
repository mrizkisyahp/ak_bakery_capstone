from app.intent.keywords import INTENT_KEYWORDS
from app.intent.schemas import IntentClassificationResult

class DummyIntentClassifier:
  PRIORITY = [
    "complaint",
    "ordering",
    "product_inquiry",
  ]
  
  def classify(self, text: str) -> IntentClassificationResult:
    normalized_text = text.lower().strip()
    
    if not normalized_text:
      return IntentClassificationResult(
        intent="other",
        confidence=0.0
      )
      
    detected_intents = []
    
    for intent in self.PRIORITY:
      keywords = INTENT_KEYWORDS[intent]
      
      if any(keyword in normalized_text for keyword in keywords):
        detected_intents.append(intent)
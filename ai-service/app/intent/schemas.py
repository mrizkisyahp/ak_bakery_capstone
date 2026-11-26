from pydantic import BaseModel, Field

class IntentClassificationResult(BaseModel):
  intent: str
  confidence: float = Field(ge=0.0, le=1.0)
  
class IntentRoutingResult(BaseModel):
  intent: str
  prompt_type: str
  confidence: float = Field(ge=0.0, le=1.0)
  fallback_applied: bool
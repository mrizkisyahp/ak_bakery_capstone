import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace

from app.rag.generation.generator import ResponseGenerator

class TestResponseGenerator(unittest.TestCase):
  
  def setUp(self):
    self.settings_patcher = patch(
      "app.rag.generation.generator.get_settings"
    )
    mock_settings = self.settings_patcher.start()
    
    mock_settings.return_value = SimpleNamespace(
      gonka_api_key=SimpleNamespace(
        get_secret_value=lambda: "fake-api-key"
      ),
      gonka_base_url="https://example.com/v1",
      llm_model="test_model"
    )
    
    self.addCleanup(self.settings_patcher.stop)
    
    with patch(
      "app.rag.generation.generator.OpenAI"
    ) as mock_openai:
      self.mock_client = Mock()
      mock_openai.return_value = self.mock_client
      
      self.generator = ResponseGenerator()
      
  def test_generate_success(self):
    self.mock_client.chat.completions.create.return_value = (
      SimpleNamespace(
        choices=[
          SimpleNamespace(
            message=SimpleNamespace(
              content="Adiskirani menjual produk bakery."
            )
          )
        ]
      )
    )
    
    context = [
      {
        "question": "Apa produk Adiskirani Bakery?",
        "answer": "Adiskirani menjual berbagai produk bakery.",
        "score": 0.90,
      }
    ]
    
    result = self.generator.generate(
      message="Apa produk Adiskirani Bakery?",
      context=context,
      prompt_type="product_inquiry",
    )
    
    self.assertEqual(
      result, 
      "Adiskirani menjual produk bakery."
    )
    self.mock_client.chat.completions.create.assert_called_once()
    
  def test_generate_empty_message_raises_error(self):
    with self.assertRaises(ValueError):
      self.generator.generate(
        message="",
        context=[{"question": "Q", "answer": "A"}],
        prompt_type="product_inquiry"
      )
    
    self.mock_client.chat.completions.create.assert_not_called()
    
  def test_generate_empty_context_raises_error(self):
    with self.assertRaises(ValueError):
      self.generator.generate(
        message="Apa produk Adiskirani Bakery?",
        context=[],
        prompt_type="product_inquiry",
      )
      
    self.mock_client.chat.completions.create.assert_not_called()
    
  def test_generate_invalid_prompt_type_raises_error(self):
    with self.assertRaises(ValueError):
      self.generator.generate(
        message="Apa produk Adiskirani Bakery?",
        context=[{"question": "Q", "answer": "A"}],
        prompt_type="unknown",
      )
    
    self.mock_client.chat.completions.create.assert_not_called()
    
  def test_generate_empty_llm_response_raises_error(self):
    self.mock_client.chat.completions.create.return_value = (
      SimpleNamespace(
        choices=[
          SimpleNamespace(
            message=SimpleNamespace(content=" ")
          )
        ]
      )
    )
    
    with self.assertRaisesRegex(
      RuntimeError,
      "LLM returned an empty response",
    ):
      self.generator.generate(
        message="Apa produk Adiskirani Bakery?",
        context=[{"question": "Q", "answer": "A"}],
        prompt_type="product_inquiry"
      )
    
  def test_format_context(self):
    context = [
      {
        "question": "Apa produk Adiskirani Bakery?",
        "answer": "Produk bakery.",
      },
      {
        "question": "Bagaimana cara memesan?",
        "answer": "Hubungi Adiskirani."
      }
    ]
    
    result = self.generator._format_context(context)
    
    self.assertIn("FAQ 1:", result)
    self.assertIn("FAQ 2:", result)
    self.assertIn("Produk bakery.", result)
    self.assertIn("Hubungi Adiskirani.", result)
      
if __name__ == "__main__":
  unittest.main()
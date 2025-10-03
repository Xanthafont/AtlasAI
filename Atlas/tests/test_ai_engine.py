import unittest
from unittest.mock import Mock, patch
from src.ai_engine import AIEngine
from src.memory_manager import MemoryManager

class TestAIEngine(unittest.TestCase):
    
    def setUp(self):
        self.memory_manager = Mock(spec=MemoryManager)
        self.ai_engine = AIEngine(self.memory_manager)
        
    @patch('src.ai_engine.OpenAI')
    def test_get_chat_response_success(self, mock_openai):
        # Mock the API response
        mock_response = Mock()
        mock_response.choices[0].message.content = "Test response"
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        response = self.ai_engine.get_chat_response(
            "Hello", "System prompt", {"conversations": [], "key_points": []}
        )
        
        self.assertEqual(response, "Test response")
    
    def test_prepare_messages(self):
        system_prompt = "Test system prompt"
        user_input = "Test user input"
        memory = {
            "conversations": [
                {"user_input": "Hi", "ai_response": "Hello"},
                {"user_input": "How are you?", "ai_response": "I'm good"}
            ],
            "key_points": [
                {"summary": "Test summary"}
            ]
        }
        
        messages = self.ai_engine._prepare_messages(user_input, system_prompt, memory)
        
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], system_prompt)
        self.assertEqual(messages[-1]["role"], "user")
        self.assertEqual(messages[-1]["content"], user_input)

if __name__ == '__main__':
    unittest.main()
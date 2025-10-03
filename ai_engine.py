import os
from openai import OpenAI
from src.utils.helpers import get_timestamp

class AIEngine:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def get_chat_response(self, user_input, system_prompt, memory):
        """Get response from OpenAI API with memory context"""
        try:
            # Prepare conversation history
            messages = self._prepare_messages(user_input, system_prompt, memory)
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            ai_response = response.choices[0].message.content
            
            # Update memory with new interaction
            self.memory_manager.update_memory(user_input, ai_response, memory)
            
            return ai_response
            
        except Exception as e:
            print(f"AI Engine Error: {e}")
            return None
    
    def _prepare_messages(self, user_input, system_prompt, memory):
        """Prepare the messages array for OpenAI API"""
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add recent context from memory
        if memory.get("key_points"):
            recent_context = "Recent context:\n" + "\n".join(
                [f"- {point['summary']}" for point in memory["key_points"][-3:]]
            )
            messages.append({"role": "system", "content": recent_context})
        
        # Add conversation history (last 10 exchanges)
        for exchange in memory.get("conversations", [])[-10:]:
            messages.append({"role": "user", "content": exchange["user_input"]})
            messages.append({"role": "assistant", "content": exchange["ai_response"]})
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        return messages
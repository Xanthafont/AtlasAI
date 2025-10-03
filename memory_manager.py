import json
import os
from datetime import datetime
from src.utils.helpers import safe_json_load, safe_json_save

class MemoryManager:
    def __init__(self, memory_file="data/memory/conversation_memory.json"):
        self.memory_file = memory_file
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """Ensure the directory for memory file exists"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
    
    def load_memory(self):
        """Load conversation memory from JSON file"""
        memory = safe_json_load(self.memory_file, {
            "conversations": [],
            "key_points": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        return memory
    
    def save_memory(self, memory):
        """Save memory to JSON file"""
        memory["updated_at"] = datetime.now().isoformat()
        safe_json_save(memory, self.memory_file)
    
    def update_memory(self, user_input, ai_response, memory):
        """Update memory with new conversation and extract key points"""
        # Add to conversation history
        memory["conversations"].append({
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "ai_response": ai_response
        })
        
        # Keep only last 50 conversations to prevent file from growing too large
        memory["conversations"] = memory["conversations"][-50:]
        
        # Extract key points from important conversations
        self._extract_key_points(user_input, ai_response, memory)
        
        # Save updated memory
        self.save_memory(memory)
    
    def _extract_key_points(self, user_input, ai_response, memory):
        """Extract and store key points from important conversations"""
        key_phrases = ["due", "deadline", "project", "important", "remember", 
                      "assignment", "homework", "task", "exam", "meeting", "appointment"]
        
        user_input_lower = user_input.lower()
        
        # Check if conversation contains important information
        if any(phrase in user_input_lower for phrase in key_phrases):
            summary = self._generate_summary(user_input)
            
            memory.setdefault("key_points", []).append({
                "timestamp": datetime.now().isoformat(),
                "summary": summary,
                "user_input": user_input[:150] + "..." if len(user_input) > 150 else user_input,
                "category": self._categorize_conversation(user_input)
            })
            
            # Keep only last 25 key points
            memory["key_points"] = memory["key_points"][-25:]
    
    def _generate_summary(self, user_input):
        """Generate a summary of important information"""
        user_lower = user_input.lower()
        
        if "due" in user_lower or "deadline" in user_lower:
            return f"Deadline mentioned: {self._extract_key_info(user_input)}"
        elif "project" in user_lower:
            return f"Project discussion: {self._extract_key_info(user_input)}"
        elif "exam" in user_lower or "test" in user_lower:
            return f"Exam/test mentioned: {self._extract_key_info(user_input)}"
        elif "meeting" in user_lower or "appointment" in user_lower:
            return f"Meeting/appointment: {self._extract_key_info(user_input)}"
        else:
            return f"Important note: {user_input[:80]}..."
    
    def _extract_key_info(self, text):
        """Extract the most relevant part of the text"""
        words = text.split()
        if len(words) > 10:
            return ' '.join(words[:10]) + "..."
        return text
    
    def _categorize_conversation(self, user_input):
        """Categorize the conversation for better organization"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ["school", "homework", "assignment", "class", "exam", "test", "study"]):
            return "academic"
        elif any(word in input_lower for word in ["project", "task", "work", "deadline", "meeting"]):
            return "work"
        elif any(word in input_lower for word in ["feel", "stress", "tired", "happy", "sad", "angry", "anxious"]):
            return "emotional"
        elif any(word in input_lower for word in ["remember", "important", "note"]):
            return "memory"
        else:
            return "general"
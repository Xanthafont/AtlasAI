import unittest
import tempfile
import os
import json
from src.memory_manager import MemoryManager

class TestMemoryManager(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.memory_file = os.path.join(self.temp_dir, "memory.json")
        self.memory_manager = MemoryManager(self.memory_file)
    
    def tearDown(self):
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_memory_new_file(self):
        memory = self.memory_manager.load_memory()
        
        self.assertIn("conversations", memory)
        self.assertIn("key_points", memory)
        self.assertIn("created_at", memory)
        self.assertEqual(len(memory["conversations"]), 0)
    
    def test_save_and_load_memory(self):
        test_memory = {
            "conversations": [{"user_input": "test", "ai_response": "response"}],
            "key_points": [{"summary": "test summary"}],
            "created_at": "2023-01-01",
            "updated_at": "2023-01-01"
        }
        
        self.memory_manager.save_memory(test_memory)
        loaded_memory = self.memory_manager.load_memory()
        
        self.assertEqual(loaded_memory["conversations"][0]["user_input"], "test")
        self.assertEqual(loaded_memory["key_points"][0]["summary"], "test summary")
    
    def test_update_memory(self):
        memory = self.memory_manager.load_memory()
        
        self.memory_manager.update_memory("Hello", "Hi there!", memory)
        
        self.assertEqual(len(memory["conversations"]), 1)
        self.assertEqual(memory["conversations"][0]["user_input"], "Hello")
        self.assertEqual(memory["conversations"][0]["ai_response"], "Hi there!")

if __name__ == '__main__':
    unittest.main()
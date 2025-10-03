import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.ai_engine import AIEngine
from src.memory_manager import MemoryManager
from src.personality import system_prompt
from src.utils.helpers import clear_screen, print_colored

def main():
    """Main function to run the AI companion terminal interface"""
    # Load environment variables
    
    
    # Initialize components
    memory_manager = MemoryManager()
    ai_engine = AIEngine(memory_manager)
    
    clear_screen()
    print_colored("Atlas AI Companion", "cyan", bold=True)
    print_colored("=" * 40, "cyan")
    print_colored("Hello! I'm Atlas, your personal companion.", "green")
    print_colored("How can I support you today?", "green")
    print_colored("(Type 'quit', 'exit', or ':q' to end our conversation)", "yellow")
    print_colored("-" * 40, "cyan")
    
    # Load conversation memory
    memory = memory_manager.load_memory()
    
    conversation_count = 0
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', ':q']:
                print_colored("Atlas: Take care!", "green")
                break
                
            if not user_input:
                continue
            
            # Get AI response
            ai_response = ai_engine.get_chat_response(user_input, system_prompt, memory)
            
            if ai_response:
                print_colored(f"Atlas: {ai_response}", "blue")
                conversation_count += 1
            else:
                print_colored("Atlas: I encountered an error. Please try again.", "red")
                
            print_colored("-" * 40, "cyan")
            
        except KeyboardInterrupt:
            print_colored("\nAtlas: Session interrupted. Goodbye! 👋", "yellow")
            break
        except Exception as e:
            print_colored(f"Atlas: An unexpected error occurred: {e}", "red")

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print_colored("Error: OPENAI_API_KEY environment variable is not set.", "red")
        print_colored("Please set your API key in the .env file:", "yellow")
        print_colored("   OPENAI_API_KEY=your-api-key-here", "yellow")
        exit(1)
    
    main()
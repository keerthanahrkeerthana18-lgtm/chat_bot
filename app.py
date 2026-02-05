import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

# Terminal colors for a nicer chat experience
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_banner():
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*50}")
    print("       🤖 Interactive AI Chatbot")
    print(f"{'='*50}{Colors.RESET}")
    print(f"{Colors.YELLOW}Type your message and press Enter to chat.")
    print(f"Type 'quit', 'exit', or 'bye' to end the conversation.{Colors.RESET}\n")

def main():
    # Configuration
    endpoint = "https://models.github.ai/inference"
    model = "gpt-4o-mini"
    
    try:
        token = os.environ["GITHUB_TOKEN"]
    except KeyError:
        print(f"{Colors.RED}Error: GITHUB_TOKEN environment variable not set!{Colors.RESET}")
        print("Please set your GitHub token: set GITHUB_TOKEN=your_token_here")
        return

    # Initialize client
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    # Conversation history (maintains context)
    conversation_history = [
        SystemMessage(content="You are a helpful, friendly, and knowledgeable assistant. Be concise but thorough in your responses.")
    ]

    print_banner()

    while True:
        try:
            # Get user input
            user_input = input(f"{Colors.GREEN}{Colors.BOLD}You: {Colors.RESET}").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print(f"\n{Colors.CYAN}👋 Goodbye! Thanks for chatting!{Colors.RESET}\n")
                break
            
            # Skip empty input
            if not user_input:
                print(f"{Colors.YELLOW}Please type a message.{Colors.RESET}")
                continue

            # Add user message to history
            conversation_history.append(UserMessage(content=user_input))

            # Get AI response
            print(f"{Colors.CYAN}{Colors.BOLD}Bot: {Colors.RESET}", end="", flush=True)
            
            response = client.complete(
                messages=conversation_history,
                temperature=0.7,
                top_p=0.95,
                max_tokens=1000,
                model=model
            )

            # Extract and display the response
            bot_response = response.choices[0].message.content
            print(bot_response)
            print()  # Add spacing between messages

            # Add assistant response to history for context
            conversation_history.append(AssistantMessage(content=bot_response))

        except KeyboardInterrupt:
            print(f"\n\n{Colors.CYAN}👋 Goodbye! Chat interrupted.{Colors.RESET}\n")
            break
        except Exception as e:
            print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}Let's try again...{Colors.RESET}\n")

if __name__ == "__main__":
    main()


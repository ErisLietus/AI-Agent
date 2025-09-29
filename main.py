import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types 
from functions.generate_content import generate_content
from config import MAX_ITERS

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Gemini error: missing GEMINI_API_KEY")
        return

    if len(sys.argv) < 2:
        print("Error: missing prompt")
        print("Usage: uv run main.py \"your prompt here\"")
        sys.exit(1)
    
    prompt = " ".join(sys.argv[1:])
    verbose = "--verbose" in sys.argv  
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    
    for i in range(MAX_ITERS):
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:  # If we got a text response, we're done
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()

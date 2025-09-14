import sys
import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Gemini error: missing GEMINI_API_KEY")
        return

    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
                print("Error: missing prompt")
                sys.exit(1)
    
    prompt = sys.argv     
    
    try:
            resp = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents= prompt
            )
            print(resp.text)
            meta = resp.usage_metadata
            print(f"Prompt tokens: {meta.prompt_token_count}")
            print(f"Response tokens: {meta.candidates_token_count}")  
    except Exception as e:
        msg = str(e).lower()
        if "quota" in msg or "exceeded" in msg or "rate limit" in msg:
            print(f"Gemini error: {e}\nHint: You may be out of free-tier tokens. Try again after the daily reset.")
        elif "401" in msg or "403" in msg or "unauthorized" in msg or "forbidden" in msg or "invalid api key" in msg:
            print(f"Gemini error: {e}\nHint: Check GEMINI_API_KEY in your .env and ensure load_dotenv() runs before use.")
        elif "timeout" in msg or "timed out" in msg or "connection" in msg:
            print(f"Gemini error: {e}\nHint: Check your internet connection and retry.")
        else:
            print(f"Gemini error: {e}")

if __name__ == "__main__":
    main()

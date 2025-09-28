import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types 
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

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
    client = genai.Client(api_key=api_key)

    messages = [

         types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,schema_get_files_content,schema_run_python_file,schema_write_file
        ]
    )

    try:
        resp = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ))
            
        if "--verbose" in prompt:  
            print(f"User prompt: {prompt[:]}")
            meta = resp.usage_metadata
            print(f"Prompt tokens: {meta.prompt_token_count}")
            print(f"Response tokens: {meta.candidates_token_count}")
        if resp.function_calls: 
            first_call = resp.function_calls[0]
            print(f"Calling function: {first_call.name}({first_call.args})")
        else:
            print(resp.text)
        meta = resp.usage_metadata

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

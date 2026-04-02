import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key not configured!")
    
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

    if response.usage_metadata is None:
        raise RuntimeError("Could not generate response. Could possibly have no tokens left.")
    prompt_token_count = response.usage_metadata.prompt_token_count
    candidates_token_count = response.usage_metadata.candidates_token_count

    if response.text is None:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")


if __name__ == "__main__":
    main()

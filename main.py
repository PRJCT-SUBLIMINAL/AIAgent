import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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

    for _ in range(20):
        response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.usage_metadata is None:
            raise RuntimeError("Could not generate response. Could possibly have no tokens left.")
        prompt_token_count = response.usage_metadata.prompt_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count

        if not response.function_calls:
            print(response.text)
            return

        function_responses = []
        for function_call in response.function_calls:
            result = call_function(function_call, verbose=args.verbose)

            if not result.parts:
                raise RuntimeError("Couldn't yield result")

            if result.parts[0].function_response is None:
                raise RuntimeError(f"Could not receive function response")

            if result.parts[0].function_response.response is None:
                raise RuntimeError(f"Could not find function response")
            
            function_responses.append(result.parts[0])

            if args.verbose:
                print(f"-> {result.parts[0].function_response.response}")
        
        messages.append(types.Content(role="user", parts=function_responses))

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_token_count}")
            print(f"Response tokens: {candidates_token_count}")
    
    print("Agent did not complete within 20 iterations.")

if __name__ == "__main__":
    main()

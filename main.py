import os
import argparse
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from config import MAX_ITERS
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="Chat Agent")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(MAX_ITERS):
        response = generate_content(client, messages)
        for candidate in response.candidates:
            messages.append(candidate.content)

        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")

        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if not response.function_calls:
            print("Response:")
            print(response.text)
            break

        function_results = []
        for function in response.function_calls:
            function_call_result = call_function(function, args.verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
                or not function_call_result.parts[0].function_response.response
            ):
                raise RuntimeError(f"Empty function response for {function.name}")
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_results.append(function_call_result.parts[0])
        messages.append(types.Content(role="user", parts=function_results))
    else:
        print(f"Max iterations ({MAX_ITERS}) reached")
        sys.exit(1)


def generate_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt, temperature=0
        ),
    )
    return response


if __name__ == "__main__":
    main()

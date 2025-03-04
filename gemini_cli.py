#!/usr/bin/env python3
import argparse
import google.generativeai as genai
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Gemini CLI tool")
    parser.add_argument("prompt", nargs="+", default=None, help="Prompt for Gemini API. If '-', read from stdin, otherwise, these are the prompts, joined by newlines.")
    parser.add_argument("--prompt", type=str, dest="prompt_option", default=None, help="Optional prompt for Gemini API (alternative to positional prompt)")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    prompt_text = ""
    if args.prompt_option: # --prompt option takes precedence
        prompt_text = args.prompt_option
    elif args.prompt and args.prompt[0] == '-':
        prompt_text = sys.stdin.read()
    elif args.prompt is not None and args.prompt[0] != '-': # positional prompt, and not '-'
        prompt_text = "\\n".join(args.prompt)
    elif not sys.stdin.isatty(): # check for pipe if no positional or --prompt option
        prompt_text = sys.stdin.read()
    elif args.prompt is None: # No prompt provided at all, check stdin again just in case of empty pipe
        if not sys.stdin.isatty():
            prompt_text = sys.stdin.read()

    if not prompt_text and not args.prompt_option:
        print("Error: Prompt is required. Please provide a prompt as an argument, using --prompt, or use '-' to read from stdin, or via pipe.")
        sys.exit(1)
    if not prompt_text and args.prompt_option:
        prompt_text = args.prompt_option
    print(prompt_text)
    response_stream = model.generate_content(prompt_text, stream=True)

    for chunk in response_stream:
        print(chunk.text, end="", flush=True)
    print() # Add newline at the end

if __name__ == "__main__":
    main()

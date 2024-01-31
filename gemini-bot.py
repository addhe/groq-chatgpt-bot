import google.generativeai as genai
import os
import sys
import argparse
import time

# Define the Gemini model ID as a constant
GEMINI_MODEL_ID = "gemini-pro"

def setup_gemini_api():
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GOOGLE Gemini API Key.")
    else:
        genai.configure(api_key=api_key)

def generate_content(prompt):
    try:
        setup_gemini_api()
        model = genai.GenerativeModel(GEMINI_MODEL_ID)
        response = model.generate_content(prompt)
        for char in response.text:
            print(char, end='', flush=True)
            time.sleep(0.02)
        #print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="The prompt to generate content for.")
    args = parser.parse_args()

    generate_content(args.prompt)

if __name__ == "__main__":
    main()

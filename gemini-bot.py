import google.generativeai as genai
import os
import sys
import argparse
import time

# Define the Gemini model ID as a constant
GEMINI_MODEL_ID = "gemini-1.5-flash"
model = genai.GenerativeModel(GEMINI_MODEL_ID)
chat = model.start_chat(history=[])

def setup_gemini_api():
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GOOGLE Gemini API Key.")
    else:
        genai.configure(api_key=api_key)

def generate_content(prompt):
    try:
        setup_gemini_api()
        response = chat.send_message(prompt)
        for char in response.text:
            print(char, end='', flush=True)
            time.sleep(0.02)
        #print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    """Main function."""
    welcoming_text = """
        Welcome to Gemini Text Generator made by (Awan),
        Happy chat and talk with your Gemini Ai Generative
        (Addhe Warman Putra - Awan)

        type 'exit()' to exit from program
    """
    print(welcoming_text)
    while True:
        prompt = input("\n> ")
        if prompt == "exit()":
            exit()
        generate_content(prompt)

if __name__ == "__main__":
    main()

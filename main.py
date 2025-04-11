import os
import time
import asyncio
import sys
from typing import Dict, List
from groq import Groq
from chat_history import ChatHistory


MAX_HISTORICAL_CONTEXT = 10


class GroqChat:
    """Chat interface with Groq API."""

    DEFAULT_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"

    def __init__(self, model_id=None):
        """Initialize the Groq API client."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY.")
        self.client = Groq(api_key=api_key)
        self.history = ChatHistory()
        self.model_id = model_id or self.DEFAULT_MODEL

    async def generate_content(
            self, prompt: str, context: List[Dict[str, str]] = None
    ) -> str:
        """Generate content based on the user prompt using Groq API."""
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        if context:
            for ctx in reversed(context):
                messages.insert(
                    0,
                    {
                        "role": "user",
                        "content": ctx["user_input"]
                    }
                )
                messages.insert(
                    0,
                    {
                        "role": "assistant",
                        "content": ctx["ai_response"]
                    }
                )
        completion = self.client.chat.completions.create(
            model=self.model_id,  # Use the custom model ID
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        content = completion.choices[0].message.content
        for char in content:
            print(char, end='', flush=True)
            await asyncio.sleep(0.02)  # Simulate typing delay
        return content

    async def chat(self):
        """Start the chat conversation."""
        welcoming_text = (
            "Welcome to {} Text Generator,\n"
            "Happy chat and talk with your {} AI Generative Model.\n"
            "Addhe Warman Putra - (Awan)\n"
            "type 'exit()' to exit from program\n"
            .format(self.model_id, self.model_id)
        )
        print(welcoming_text)

        while True:
            user_input = input("\n> ")
            if user_input.lower() == "exit()":
                break
            ai_response = await self.generate_content(
                user_input, self.history.get_context()
            )
            print()  # Move to a new line after AI response
            self.history.add_context(user_input, ai_response)


async def main():
    """Main function to start the chat with Groq API."""
    model_id = None
    if len(sys.argv) > 1:
        model_id = sys.argv[1]
    
    chat = GroqChat(model_id)
    await chat.chat()


if __name__ == "__main__":
    asyncio.run(main())

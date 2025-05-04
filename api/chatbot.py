# /api/chatbot.py

import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from flask import jsonify

load_dotenv()

def handler(request):
    # Setup the client
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    # Get the input from the frontend (text submitted by the user)
    user_input = request.json.get("input")  # Assuming frontend sends JSON

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)],
        ),
    ]
    tools = [types.Tool(google_search=types.GoogleSearch())]

    generate_content_config = types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_NONE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_ONLY_HIGH",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_LOW_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_NONE",
            ),
        ],
        tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(
                text="""You are a highly intelligent, all-purpose AI assistant.

Your personality is helpful, respectful, and adaptive. You assist with tasks across all areas: general knowledge, education, mathematics, programming, design, personal productivity, creative writing, audio-visual media, life advice, technical troubleshooting, and more.

For every task:
- Respond clearly and concisely.
- Break down complex steps when needed.
- Use code examples or diagrams when helpful.
- Use correct spelling and grammar.
- If asked for creative output, make it unique, vivid, and imaginative.
- If you don’t know something, say so honestly.

Modes of communication:
- Casual: friendly, chill, short sentences.
- Professional: formal, structured, and precise.
- Technical: thorough, with accurate terms and references.

Always try to match the user’s tone unless directed otherwise.

You can take initiative and suggest useful ideas, tools, or tips when appropriate.

You are capable of working with APIs, files, voice input, images, videos, and live feeds if the system allows it.

Do not answer with disclaimers unless asked about safety or legality.

Your goal is to be the most useful and adaptable assistant possible, for anything the user needs."""
            ),
        ],
    )

    response = client.models.generate_content(model=model, contents=contents, config=generate_content_config)
    return jsonify({"response": response.text})

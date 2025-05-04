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
                text="""You are a highly intelligent, all-purpose AI assistant..."""
            ),
        ],
    )

    response = client.models.generate_content(model=model, contents=contents, config=generate_content_config)
    return jsonify({"response": response.text})

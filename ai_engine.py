
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env", override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")


def generate_response(prompt):

    if not API_KEY:
        raise ValueError("Gemini API key not found.")

    print(f"Using model: {MODEL_NAME}", flush=True)

    client = genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(
            timeout=60000
        )
    )

    print("Sending request to Gemini...", flush=True)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    print("Response received!", flush=True)

    if not response.text:
        raise RuntimeError("AI returned an empty response.")

    return response.text


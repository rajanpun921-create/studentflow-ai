
import os
import logging
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env", override=False)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_config(name, default=None):
    try:
        value = st.secrets.get(name)
        if value:
            return value
    except Exception:
        pass

    return os.getenv(name, default)


def generate_response(prompt):

    try:
        API_KEY = get_config("GEMINI_API_KEY")

        MODEL_NAME = get_config(
            "GEMINI_MODEL",
            "gemini-3.5-flash-lite"
        )

        if not API_KEY:
            raise ValueError("Gemini API key not found.")

        print("Gemini API key detected.", flush=True)
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

        if not response.text:
            raise RuntimeError("AI returned an empty response.")

        print("Response received!", flush=True)

        return response.text

    except Exception as e:
        logger.error(
            "Gemini error: %s | Status: %s",
            type(e).__name__,
            getattr(e, "code", "Unknown")
        )
        raise

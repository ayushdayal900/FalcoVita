import os
import google.generativeai as genai
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, 'backend', '.env'))

key = os.environ.get("GOOGLE_API_KEY")
if key:
    genai.configure(api_key=key)
    print("Available Gemini Models:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")
else:
    print("GOOGLE_API_KEY missing")

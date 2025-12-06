import os
import requests
from dotenv import load_dotenv

# Load env vars
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

def test_google():
    key = os.environ.get("GOOGLE_API_KEY")
    if not key:
        print("[FAIL] GOOGLE_API_KEY is missing.")
        return
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say 'OK'")
        print(f"[PASS] Google Gemini: Works! Response: {response.text.strip()}")
    except Exception as e:
        print(f"[FAIL] Google Gemini: Error - {e}")

def test_pinecone():
    key = os.environ.get("PINECONE_API_KEY")
    if not key:
        print("[FAIL] PINECONE_API_KEY is missing.")
        return

    try:
        from pinecone import Pinecone
        pc = Pinecone(api_key=key)
        indexes = pc.list_indexes()
        print(f"[PASS] Pinecone: Works! Indexes: {[i.name for i in indexes]}")
    except Exception as e:
        print(f"[FAIL] Pinecone: Error - {e}")

def test_elevenlabs():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        print("[FAIL] ELEVENLABS_API_KEY is missing.")
        return

    try:
        url = "https://api.elevenlabs.io/v1/voices"
        headers = {"xi-api-key": key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("[PASS] ElevenLabs: Works! Voices fetched.")
        else:
            print(f"[FAIL] ElevenLabs: Status {response.status_code}")
    except Exception as e:
        print(f"[FAIL] ElevenLabs: Error - {e}")

if __name__ == "__main__":
    print("=== Testing API Keys ===")
    test_google()
    test_pinecone()
    test_elevenlabs()

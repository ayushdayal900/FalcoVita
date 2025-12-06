try:
    import google.generativeai as genai
    print("SUCCESS: google.generativeai is installed and importable.")
    print(f"Version: {genai.__version__}")
except ImportError:
    print("FAILURE: google.generativeai is NOT installed.")
except Exception as e:
    print(f"ERROR: {e}")

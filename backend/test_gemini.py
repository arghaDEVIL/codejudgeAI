"""
Quick test script to verify Gemini API is working
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {bool(api_key)}")
print(f"API Key (first 10 chars): {api_key[:10] if api_key else 'None'}...")

if not api_key:
    print("❌ No API key found in .env file")
    exit(1)

try:
    print("\n🔧 Configuring Gemini...")
    genai.configure(api_key=api_key)

    print("📋 Listing available models...")
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            print(f"  ✅ {model.name}")

    print("\n🚀 Testing gemini-2.5-flash model...")
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content("Say 'Hello, I am working!' in one sentence.")
    print(f"\n✅ SUCCESS! Response: {response.text}")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback

    traceback.print_exc()

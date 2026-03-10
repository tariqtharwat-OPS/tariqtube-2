import os
import google.generativeai as genai

def test_gemini_legacy_sdk():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "tariq-worker-key.json"
    
    # Configure the SDK
    # By default it uses ADC if no API key is provided
    
    print("Testing Gemini via legacy SDK (models/gemini-3.1-pro-preview)...")
    model = genai.GenerativeModel('models/gemini-3.1-pro-preview')
    
    response = model.generate_content("Write a 1-sentence catchy title for a children's story about a brave kitten.")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    try:
        test_gemini_legacy_sdk()
        print("Gemini test successful!")
    except Exception as e:
        print(f"Gemini test failed: {e}")

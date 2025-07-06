import requests
import json

def test_api(text, api_url="http://localhost:8000/translate"):
    """Test the translation API"""
    
    payload = {
        "text": text,
        "num_beams": 4,
        "max_length": 128
    }
    
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"Original: {result['original_text']}")
        print(f"Translation: {result['translated_text']}")
        print(f"Beams: {result['num_beams']}")
        print("-" * 50)
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

if __name__ == "__main__":
    # Test sentences
    test_sentences = [
        "Hello, how are you?",
        "I love learning new languages.",
        "The weather is beautiful today.",
        "What time is it?",
        "Thank you for your help."
    ]
    
    print("Testing Neural Machine Translation API...")
    print("Make sure the API is running on http://localhost:8000")
    print("="*60)
    
    for sentence in test_sentences:
        test_api(sentence)

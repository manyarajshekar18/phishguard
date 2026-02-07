import os
import requests
import json

API_KEY = os.getenv('GOOGLE_API_KEY')

BASE_URL = 'https://generativelanguage.googleapis.com/v1beta'

def detect_phishing(url: str) -> dict:
    if not API_KEY:
        return {'isPhishing': False, 'confidence': 0, 'reasons': ['API key not set']}
    models = ['gemini-1.5-flash', 'gemini-1.5-pro']
    for model in models:
        try:
            response = requests.post(
                f'{BASE_URL}/models/{model}:generateContent?key={API_KEY}',
                headers={'Content-Type': 'application/json'},
                data=json.dumps({
                    'contents': [{
                        'parts': [{
                            'text': f'Analyze the following URL for potential phishing indicators. Provide a JSON response with fields: isPhishing (boolean), confidence (number 0-100), reasons (array of strings explaining the analysis).\n\nURL: {url}'
                        }]
                    }]
                })
            )
            if response.status_code == 200:
                data = response.json()
                text = data['candidates'][0]['content']['parts'][0]['text']
                result = json.loads(text)
                return result
            else:
                print(f'Error with model {model}: {response.status_code} {response.text}')
        except Exception as e:
            print(f'Exception with model {model}: {e}')
    return {'isPhishing': False, 'confidence': 0, 'reasons': ['Detection failed']}

# Example usage
if __name__ == '__main__':
    result = detect_phishing('http://example.com')
    print(result)

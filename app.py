from flask import Flask, request, jsonify, send_from_directory
from ai_engine.gemini import detect_phishing

app = Flask(__name__, static_folder='public')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory('public/assets', path)

@app.route('/api/detect', methods=['POST'])
def detect():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    try:
        result = detect_phishing(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

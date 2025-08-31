from flask import Flask, jsonify, request, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Test Server Working!</h1><p>Flask is running correctly.</p>'

@app.route('/simple')
def simple():
    try:
        return render_template('simple.html')
    except Exception as e:
        return f'Template error: {e}'

@app.route('/test', methods=['POST'])
def test():
    try:
        data = request.json
        return jsonify({'received': data, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting test server on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=True)

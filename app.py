from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# List to store log messages
logs = []

# Directory path for your HTML files
html_dir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def home():
    return "Hello, Flask is running!"

# Route to serve buttons.html
@app.route('/buttons')
def buttons_page():
    return send_from_directory(html_dir, 'buttons.html')

# Route to serve logs.html
@app.route('/logs_page')
def logs_page():
    return send_from_directory(html_dir, 'logs.html')

# Route to handle button actions
@app.route('/buttons', methods=['POST'])
def handle_button():
    data = request.get_json()
    action = data.get('action')
    if action:
        log_message = f"Action received: {action}"
        print(log_message)
        logs.append(log_message)
    return jsonify({"status": "success", "action": action}), 200

# Route to serve logs data for logs.html
@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(logs[-10:])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123, debug=True)

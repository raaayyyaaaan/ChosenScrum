from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Directory path for your HTML files
html_dir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def home():
    return "Hello, Flask is running!"

@app.route('/buttons')
def buttons_page():
    return app.send_static_file('buttons.html')

@app.route('/logs_page')
def logs_page():
    return app.send_static_file('logs.html')

@app.route('/buttons', methods=['POST'])
def handle_button():
    data = request.get_json()
    action = data.get('action')
    if action:
        log_message = f"Action received: {action}"
        print(log_message)
        logs.append(log_message)

    return jsonify({"status": "success", "action": action}), 200

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(logs[-10:])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123, debug=True)

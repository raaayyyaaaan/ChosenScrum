from flask import Flask, request, jsonify

app = Flask(__name__)

# List to store log messages
logs = []

# Basic test route to confirm the server is running
@app.route('/')
def home():
    return "Hello, Flask is running!"

# Route to handle button actions
@app.route('/buttons', methods=['POST'])
def handle_button():
    data = request.get_json()
    action = data.get('action')
    
    # Log the action
    if action:
        log_message = f"Action received: {action}"
        print(log_message)  # This prints to the terminal
        logs.append(log_message)  # Add log message to logs list

    return jsonify({"status": "success", "action": action}), 200

# Route to serve logs (for logs.html)
@app.route('/logs', methods=['GET'])
def get_logs():
    # Return the logs as JSON to be displayed on logs.html
    return jsonify(logs[-10:])  # Only show the last 10 logs for simplicity

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123, debug=True)

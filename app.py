from flask import Flask, request, jsonify

app = Flask(__name__)

# Basic test route to confirm the server is running
@app.route('/')
def home():
    return "Hello, Flask is running!"

# Route to handle button actions
@app.route('/buttons', methods=['POST'])
def handle_button():
    data = request.get_json()
    action = data.get('action')
    
    # Perform actions based on button press (logging or controlling the robot)
    if action == "fwd":
        print("Moving Forward")
    elif action == "bwd":
        print("Moving Backward")
    elif action == "left":
        print("Turning Left")
    elif action == "right":
        print("Turning Right")
    elif action == "stop":
        print("Stopping")
    
    return jsonify({"status": "success", "action": action}), 200

# Route to serve logs (for logs.html)
@app.route('/logs', methods=['GET'])
def get_logs():
    # This would normally fetch logs from a database or file
    logs = ["Log 1: Movement", "Log 2: Stopped"]
    return jsonify(logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123, debug=True)

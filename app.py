from flask import Flask, request, jsonify, render_template
from datetime import datetime
import json
import os

app = Flask(__name__)

# Create logs directory if it doesn't exist
LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'robot_logs.json')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def save_log(action):
    """Save log entry to JSON file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "action": action,
    }
    
    try:
        # Read existing logs
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        # Add new log entry
        logs.append(log_entry)
        
        # Keep only last 100 logs to prevent file from growing too large
        logs = logs[-100:]
        
        # Save updated logs
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f)
            
    except Exception as e:
        print(f"Error saving log: {e}")

@app.route('/')
def home():
    return render_template('buttons.html')

@app.route('/buttons', methods=['POST'])
def handle_button():
    data = request.get_json()
    action = data.get('action')
    
    actions = {
        "fwd": "Moving Forward",
        "bwd": "Moving Backward",
        "left": "Turning Left",
        "right": "Turning Right",
        "stop": "Stopping"
    }
    
    if action in actions:
        message = actions[action]
        print(message)  # For console logging
        save_log(message)  # Save to file
        return jsonify({"status": "success", "action": action}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid action"}), 400

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
                # Return last 50 logs in reverse chronological order
                return jsonify(logs[-50:][::-1])
        return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123)

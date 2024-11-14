from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Create or clear the log file when starting
LOG_FILE = 'robot_logs.txt'
with open(LOG_FILE, 'w') as f:
    f.write("=== Robot Control Logs ===\n")

def log_action(action):
    """Write action to log file"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}: {action}\n"
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)
    print(log_entry.strip())  # Also print to terminal

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Robot Control</title>
        <style>
            .button-grid {
                display: grid;
                grid-template-columns: repeat(3, 60px);
                gap: 10px;
                margin: 20px auto;
                width: fit-content;
            }
            button {
                padding: 15px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="button-grid">
            <button></button>
            <button onclick="sendCommand('fwd')">↑</button>
            <button></button>
            <button onclick="sendCommand('left')">←</button>
            <button onclick="sendCommand('stop')">■</button>
            <button onclick="sendCommand('right')">→</button>
            <button></button>
            <button onclick="sendCommand('bwd')">↓</button>
            <button></button>
        </div>

        <script>
            function sendCommand(action) {
                fetch('/buttons', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ action: action })
                });
            }
        </script>
    </body>
    </html>
    """

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
        log_action(message)
        return jsonify({"status": "success"}), 200
    
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123)

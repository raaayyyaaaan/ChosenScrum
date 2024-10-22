# The flask module allows us to create a flask framework, which we can use to send requests using http requests.
# The time module allows us to fix the duration of time each function moves by seconds.
# The adafruit_pca9685 module allows us to control how much electrical power needs to be sent
# The board module allows us to access a series of board-specific objects on the raspberry pi, such as pins.
# The busio module handles I2C communication
from flask import Flask, request, jsonify
import time
from PCA9685 import PCA9685

pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(20)


app = Flask(__name__)

# The TankRobot class allows us to connect to the motors and control the amount of electrical power being sent to each of the motors. It also has the functions to get the tank to move forward, backward, left, right, and stop.
class TankRobot:
    def __init__(self):
        self.PWMA = 0 # Controls the power supplied and connects it to hardware
        self.AIN1 = 1 # Controls direction of the first motor
        self.AIN2 = 2 # Controls the opposite direction of the first motor
        self.PWMB = 5 # Controls the power supplied and connects it to hardware
        self.BIN1 = 3 # Controls direction of the second motor
        self.BIN2 = 4 # Controls the opposite direction of the second motor

# Gets the tank to move forward for three seconds before stopping, taking in speed as a parameter
    def move_fwd(self, speed):
        pwm.setDutycycle(self.PWMA, speed)
        pwm.setLevel(self.AIN1, 0)
        pwm.setLevel(self.AIN2, 1)
        pwm.setDutycycle(self.PWMB, speed)
        pwm.setLevel(self.BIN1, 1)
        pwm.setLevel(self.BIN2, 0)
        time.sleep(0.25)
        self.stop()

# Gets the tank to move backward for three seconds before stopping, taking in speed as a parameter.
    def move_backward(self, speed):
        pwm.setDutycycle(self.PWMA, speed)
        pwm.setLevel(self.AIN1, 1) # Left motor goes backwards
        pwm.setLevel(self.AIN2, 0)
        pwm.setDutycycle(self.PWMB, speed)
        pwm.setLevel(self.BIN1, 0) #Right motor goes forwards
        pwm.setLevel(self.BIN2, 1)
        time.sleep(0.25)
        self.stop()

# Gets the tank to turn left for three seconds before stopping, taking in speed as a parameter.
    def turn_left(self, speed):
        pwm.setDutycycle(self.PWMA, speed)
        pwm.setLevel(self.AIN1, 1)
        pwm.setLevel(self.AIN2, 0)   # Left motor goes backward
        pwm.setDutycycle(self.PWMB, speed)
        pwm.setLevel(self.BIN1, 1)
        pwm.setLevel(self.BIN2, 0)  # Right motor goes forward
        time.sleep(0.2)
        self.stop()

# Gets the tank to turn right for three seconds before stopping, taking in speed as a parameter.
    def turn_right(self, speed):
        pwm.setDutycycle(self.PWMA, speed) # Left motor goes forward
        pwm.setLevel(self.AIN1, 0)
        pwm.setLevel(self.AIN2, 1)
        pwm.setDutycycle(self.PWMB, speed) # Right motor goes backward
        pwm.setLevel(self.BIN1, 0)
        pwm.setLevel(self.BIN2, 1)
        time.sleep(0.2)
        self.stop()


# Gets the tank to stop, taking in no parameters
    def stop(self):
        pwm.setDutycycle(self.PWMA, 0)  # Stop left motor
        pwm.setDutycycle(self.PWMB, 0)  # Stop right motor
        time.sleep(0.25)
        self.stop()

tank_robot = TankRobot()


# We created a POST route with no parameters, then ran the move_fwd command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/fwd', methods=['POST'])
def fwd():
    tank_robot.move_fwd(50) # Move forward at speed 100
    return jsonify({'Move forward': True}) # Return confirmation that the function was ran

# We create the bwd command. We created a POST route with no parameters, then ran the move_bwd command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/bwd', methods=['POST'])
def bwd():
    tank_robot.move_backward(50) # Move backward at speed 100
    return jsonify({'Move backward': True}) # Return confirmation that the function was ran

# We create the right command. We created a POST route with no parameters, then ran the move_right command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/right', methods=['POST'])
def right():
    tank_robot.turn_right(50) # Turn right at speed 100
    return jsonify({'Turn right': True}) # Return confirmation that the function was ran

# We create the left command. We created a POST route with no parameters, then ran the move_left command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/left', methods=['POST'])
def left():
    tank_robot.turn_left(50) # Turn left at speed 100
    return jsonify({'Turn left': True}) # Return confirmation that the function was ran

# We create the stop command. We created a POST route with no parameters, then ran the stop command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/stop', methods=['POST'])
def stop():
    tank_robot.stop() # Stop
    return jsonify({'command': 'STOP'}) # Return confirmation that the function was ran


if __name__ == "__main__": # This runs the API
    app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=False) # Where the API will be hosted

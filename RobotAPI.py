# The flask module allows us to create a flask framework, which we can use to send requests using http requests.
# The time module allows us to fix the duration of time each function moves by seconds.
# The adafruit_pca9685 module allows us to control how much electrical power needs to be sent
# The board module allows us to access a series of board-specific objects on the raspberry pi, such as pins.
# The busio module handles I2C communication
from flask import Flask, request, jsonify
import time
from PCA9685 import PCA9685

pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(40)


app = Flask(__name__)

# The TankRobot class allows us to connect to the motors and control the amount of electrical power being sent to each of the motors. It also has the functions to get the tank to move forward, backward, left, right, and stop.
class TankRobot:
    def __init__(self):
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4

# Gets the tank to move forward for two seconds before stopping
    def move_fwd(self, motor, speed):
        pwm.setDutycycle(self.PWMA, speed)
        pwm.setLevel(self.AIN1, 0)
        pwm.setLevel(self.AIN2, 1)

# Gets the tank to move backward for two seconds before stopping
    def move_backward(self, motor, speed):
        pwm.setDutycycle(self.PWMA, speed)
        pwm.setLevel(self.AIN1, 1)
        pwm.setLevel(self.AIN2, 0)

# Gets the tank to turn left for two seconds before stopping
    def turn_left(self):
        self.set_motor_pwm(self.motor1_channel, 0)      # Stop left motor
        self.set_motor_pwm(self.motor2_channel, 4095)   # Full speed right
        time.sleep(2)
        self.stop()


# Gets the tank to turn right for two seconds before stopping
    def turn_right(self):
        self.set_motor_pwm(self.motor1_channel, 4095)   # Full speed left
        self.set_motor_pwm(self.motor2_channel, 0)      # Stop right motor
        time.sleep(2)
        self.stop()


# Gets the tank to stop
    def stop(self):
        self.set_motor_pwm(self.motor1_channel, 0)  # Stop motor 1
        self.set_motor_pwm(self.motor2_channel, 0)  # Stop motor 2


tank_robot = TankRobot()


# We created a POST route with no parameters, then ran the move_fwd command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/fwd', methods=['POST'])
def fwd():
    tank_robot.move_fwd(0, 100)
    return jsonify({'Move forward': True})

# We create the bwd command. We created a POST route with no parameters, then ran the move_bwd command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/bwd', methods=['POST'])
def bwd():
    tank_robot.move_backward()
    return jsonify({'Move backward': True})

# We create the right command. We created a POST route with no parameters, then ran the move_right command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/right', methods=['POST'])
def right():
    tank_robot.turn_right()
    return jsonify({'Turn right': True})

# We create the left command. We created a POST route with no parameters, then ran the move_left command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/left', methods=['POST'])
def left():
    tank_robot.turn_left()
    return jsonify({'Turn left': True})

# We create the stop command. We created a POST route with no parameters, then ran the stop command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/stop', methods=['POST'])
def stop():
    tank_robot.stop()
    return jsonify({'command': 'STOP'})


if __name__ == "__main__": # This runs the API
    app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=False) # Where the API will be hosted

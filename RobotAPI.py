from flask import Flask, request, jsonify, render_template, redirect, url_for
import time
from adafruit_motorkit import Motorkit

app = Flask(__name__)


class TankRobot:
    def __init__(self):
        self.robot = Motorkit(0x40)

    def move_fwd(self):
        self.robot.motor1.throttle = 0.5
        self.robot.motor2.throttle = 0.5

    def move_backward(self):
        self.robot.motor1.throttle = -0.5
        self.robot.motor2.throttle = -0.5

    def turn_left(self):
        self.robot.motor1.throttle = 0.0
        self.robot.motor2.throttle = 0.5

    def turn_right(self):
        self.robot.motor1.throttle = 0.5
        self.robot.motor2.throttle = 0.0


    def stop(self):
        self.robot.motor1.throttle = 0.0
        self.robot.motor2.throttle = 0.0


tank_robot = TankRobot()



#fwd() will not take in any parameters. It will output the new coordinates of the robot, where the y coordinate will be updated, and confirmation that the request was successfully processed.
@app.route('/fwd', methods = ['POST']) #Creating an api with the post method. The post method sends a request to the server to be processed
def fwd():
  out = {} #What the API will return as the output
  tank_robot.move_fwd()
  out['Move forward']=True #Shows whether it was successful
  return jsonify(out) #Returns the JSON output

#bwd() will not take in any parameters. It will output the new coordinates of the robot, where the y coordinate will be updated, and confirmation that the request was successfully processed.
@app.route('/bwd', methods = ['POST']) #Creating the backward command API
def bwd():
  out = {}
  tank_robot.move_backward()
  out['Move backward']=True
  return jsonify(out)

#right() will not take in any parameters. It will output the new coordinates of the robot, where the x coordinate will be updated, and confirmation that the request was successfully processed.
@app.route('/right', methods = ['POST']) #Creating the right command API
def right():
  out = {}
  tank_robot.turn_right()
  out['Turn right']=True
  return jsonify(out)

#left() will not take in any parameters. It will output the new coordinates of the robot, where the x coordinate will be updated, and confirmation that the request was successfully processed.
@app.route('/left', methods = ['POST']) #Creating the left command API
def left():
  out = {}
  tank_robot.turn_left()
  out['Turn left']=True
  return jsonify(out)

#stop() will not take in any parameters. It will output the final coordinates of the robot before resetting its coordinates to the origin, (0,0). It will also confirm that the STOP command was run successfully.
@app.route('/stop', methods = ['POST']) #Creating the stop command API
def stop():
  out = {}
  tank_robot.stop()
  out["command"]="STOP" #Shows that the STOP command was run

  return jsonify(out)


if __name__=="__main__": #Runs the API
  app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=False) #Where the API will be hosted, host will be updated to static raspberry pi ip address

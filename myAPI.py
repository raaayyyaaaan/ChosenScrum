from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

x = 0 #x-coordinate of where the robot is located. for reference, the origin will be located at (0,0)
y = 0 #y-coordinate of where the robot is located

#fwd() will not take in any parameters. It will output the new coordinates of the robot, where the y coordinate will be updated, and confirmation that the request was successfully processed.
@app.route('/fwd/<int:speed>/<int:time>', methods = ['POST']) #Creating an api with the post method. The post method sends a request to the server to be processed
def fwd(speed, time):
  out = {}
  bin_speed = '{0:08b}'.format(speed)
  bin_time = '{0:08b}'.format(time)
  final_str = bin_speed + bin_time
  out["forward"] = '00'+final_str
  global y
  y+=speed*time #Updating the y-coordinate. For example, if you start at (0,0), after running forward command, you get (0,1), then (0,2) after running it again.
  out["coordinates"] = f'({x},{y})' #Shows that the forward command was run; shows the coordinate after running the function
  out['success']=True #Shows whether it was successful
  return jsonify(out) #Returns the JSON output


#to run fwd with speed=10 and time=20: curl -X POST http://127.0.0.1:5000/fwd/10/20
#bwd() will not take in any parameters. It will output the new coordinates of the robot, where the y coordinate will be updated, and confirmation that the request was successfully processed.
@app.route('/bwd/<int:speed>/<int:time>', methods = ['POST']) #Creating the backward command API
def bwd(speed, time):
  global y
  y-=speed*time
  out = {}
  bin_speed = '{0:08b}'.format(speed)
  bin_time = '{0:08b}'.format(time)
  final_str = bin_speed + bin_time
  out["backward"] = '11'+final_str
  out["coordinates"] = f'({x},{y})'
  out['success']=True
  return jsonify(out)

#right() will not take in any parameters. It will output the new coordinates of the robot, where the x coordinate will be updated, and confirmation that the request was successfully processed.
@app.route('/right/<int:speed>/<int:time>', methods = ['POST']) #Creating the right command API
def right(speed, time):
  global x
  x+=speed*time
  out = {}
  bin_speed = '{0:08b}'.format(speed)
  bin_time = '{0:08b}'.format(time)
  final_str = bin_speed + bin_time
  out['right']='01'+final_str
  out["coordinates"] = f'({x},{y})'
  out['success']=True
  return jsonify(out)

#left() will not take in any parameters. It will output the new coordinates of the robot, where the x coordinate will be updated, and confirmation that the request was successfully processed.
@app.route('/left/<int:speed>/<int:time>', methods = ['POST']) #Creating the left command API
def left(speed, time):
  global x
  x-=speed*time
  out = {}
  bin_speed = '{0:08b}'.format(speed)
  bin_time = '{0:08b}'.format(time)
  final_str = bin_speed + bin_time
  out['left']='10'+final_str
  out["coordinates"] = f'({x},{y})'
  out['success']=True
  return jsonify(out)

#stop() will not take in any parameters. It will output the final coordinates of the robot before resetting its coordinates to the origin, (0,0). It will also confirm that the STOP command was run successfully.
@app.route('/stop', methods = ['POST']) #Creating the stop command API
def stop():
  global x
  global y
  out = {}
  out["command"]="STOP" #Shows that the STOP command was run
  out["final coordinates"] = f'({x},{y})' #Shows what the final coordinates were before the STOP function sets it to (0,0)
  out['success']=True
  x=0 #Sets the x-coordinate back to the origin
  y=0 #Sets the y-coordinate back to the origin

  return jsonify(out)


if __name__=="__main__": #Runs the API
  app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=False) #Where the API will be hosted
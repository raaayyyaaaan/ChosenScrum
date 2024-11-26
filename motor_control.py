from PCA9685 import PCA9685
import time

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

def motor_forward():
    pwm.setDutyCycle(4, 100)  # MA1
    pwm.setDutyCycle(5, 0)    # MA2
    pwm.setDutyCycle(6, 100)  # MB1
    pwm.setDutyCycle(7, 0)    # MB2

def motor_backward():
    pwm.setDutyCycle(4, 0)    # MA1
    pwm.setDutyCycle(5, 100)  # MA2
    pwm.setDutyCycle(6, 0)    # MB1
    pwm.setDutyCycle(7, 100)  # MB2

def motor_stop():
    pwm.setDutyCycle(4, 0)
    pwm.setDutyCycle(5, 0)
    pwm.setDutyCycle(6, 0)
    pwm.setDutyCycle(7, 0)

try:
    print("Forward")
    motor_forward()
    time.sleep(2)
    
    print("Backward")
    motor_backward()
    time.sleep(2)
    
    print("Stop")
    motor_stop()

except KeyboardInterrupt:
    print("Stopped by user")
    motor_stop()

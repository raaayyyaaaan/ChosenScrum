import time

# Import the necessary library for the Waveshare HAT
# (Replace with the actual library name)
import waveshare_hat

# Initialize the motor driver HAT
motor_driver = waveshare_hat.MotorDriver()

# Function to control motor direction and speed
def set_motor(motor, forward, speed):
    if motor == "A":
        if forward:
            motor_driver.motorA_forward(speed)
        else:
            motor_driver.motorA_backward(speed)
    elif motor == "B":
        if forward:
            motor_driver.motorB_forward(speed)
        else:
            motor_driver.motorB_backward(speed)

# Example usage:
try:
    while True:
        set_motor("A", True, 100)  # Motor A forward
        set_motor("B", True, 100)  # Motor B forward
        time.sleep(2)
        set_motor("A", False, 100)  # Motor A backward
        set_motor("B", False, 100)  # Motor B backward
        time.sleep(2)
except KeyboardInterrupt:
    # Stop the motors
    motor_driver.stop()
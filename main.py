#Dependencies
from machine import Pin, PWM, I2C
import time
from mpu6050.mpu6050 import init_mpu6050, get_mpu6050_data
from controller.motorspeed import set_motor_speed as set_motor_speed
from controller.PID_controller import PID_controller as PID_controller
from controller.map_pid import map_pid_output_to_pwm as map_pid_output_to_pwm
from mpu6050.complementary_filter import complementary_filter as complementary_filter

# Declare pwm pins for BLDC motors. 
pwm_pin1 = PWM(Pin(15))  # First motor
pwm_pin2 = PWM(Pin(16))  # Second motor
pwm_pin1.freq(60) #Frequency of pwm for each motor. 
pwm_pin2.freq(60)

# Initialize MPU6050
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
init_mpu6050(i2c)

# Declare PID controller. 
pid = PID_controller(Kp=3, Ki=7, Kd=0.001, setpoint=0, dt=0.001)

try:
    while True:
        #Pass mpu6050 data through a complementary filter to reduce noise.     
        com_fil = complementary_filter(get_mpu6050_data(i2c)['accel'], get_mpu6050_data(i2c)['gyro'], dt = 0.001, alpha = 0.5, roll = 0.0, pitch = 0.0)
        
        # Update pid_output with respect to complementary filter - Output is scaled. 
        pid_output = pid.update(com_fil['roll'])
        
        # Convert scaled value to mapping of min/max output of BLDC motors. 
        pwm_value1 = map_pid_output_to_pwm(pid_output, 3800, 4400)  # For first motor
        pwm_value2 = map_pid_output_to_pwm(-pid_output, 3800, 4400)  # For second motor, inverted
        
        
        #Set the speed of both BLDC motors. 
        set_motor_speed(pwm_value1, pwm_value2, pwm_pin1, pwm_pin2)
except KeyboardInterrupt:
        set_motor_speed(3200, 3200, pwm_pin1, pwm_pin2)  # Stop both motors
    


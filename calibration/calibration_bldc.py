from machine import Pin, PWM
import time

# Initialize PWM pin for the ESC
pwm_pin = PWM(Pin(15))
pwm_pin2 = PWM(Pin(16))
pwm_pin.freq(60)
pwm_pin2.freq(60)

def set_motor_speed(pulse_width):
    #Duty cycle for each pin
    pwm_pin.duty_u16(pulse_width)
    pwm_pin2.duty_u16(pulse_width)

# Calibration sequence
def calibrate_esc():
    print("Calibration started.")
    set_motor_speed(4400)  # Setting maximum pulse width
    time.sleep(2)
    set_motor_speed(3200)  # Setting minimum pulse width
    time.sleep(2)
    print("Calibration complete.")

try:
    calibrate_esc() #Begin calibration.
except KeyboardInterrupt: 
    set_motor_speed(3200) #End calibration. 




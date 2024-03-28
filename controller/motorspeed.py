#Motor speed
def set_motor_speed(motor1_pulse, motor2_pulse, pin_1, pin_2):
    pin_1.duty_u16(motor1_pulse)
    pin_2.duty_u16(motor2_pulse)
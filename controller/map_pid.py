#Scaled PID output
def map_pid_output_to_pwm(pid_output, min_pwm, max_pwm):
    # Assuming PID output ranges from -1 to 1, map to PWM range
    return int((pid_output * 2  + 1) / 2 * (max_pwm - min_pwm) + min_pwm)
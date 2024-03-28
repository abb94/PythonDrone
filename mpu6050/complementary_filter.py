import math

def complementary_filter(accel_data, gyro_data, dt, alpha, roll, pitch):
    # Compute orientation from accelerometer data
    roll_acc = math.atan2(accel_data['y'], accel_data['z'])
    pitch_acc = math.atan2(-accel_data['x'], math.sqrt(accel_data['y']**2 + accel_data['z']**2))
    
    # Integrate gyro data to estimate orientation change
    roll_gyro = gyro_data['x'] * dt
    pitch_gyro = gyro_data['y'] * dt
    
    # Combine accelerometer and gyro data using complementary filter
    roll = alpha * (roll + roll_gyro) + (1 - alpha) * roll_acc
    pitch = alpha * (pitch + pitch_gyro) + (1 - alpha) * pitch_acc
    
    return {'roll': roll, 'pitch': pitch}

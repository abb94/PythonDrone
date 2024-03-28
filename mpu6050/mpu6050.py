from machine import Pin, I2C
import utime
import math

PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
TEMP_OUT_H = 0x41
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

def init_mpu6050(i2c, address=0x68):
    i2c.writeto_mem(address, PWR_MGMT_1, b'\x00')
    utime.sleep_ms(100)
    i2c.writeto_mem(address, SMPLRT_DIV, b'\x07')
    i2c.writeto_mem(address, CONFIG, b'\x00')
    i2c.writeto_mem(address, GYRO_CONFIG, b'\x00')
    i2c.writeto_mem(address, ACCEL_CONFIG, b'\x00')

def read_raw_data(i2c, addr, address=0x68):
    high = i2c.readfrom_mem(address, addr, 1)[0]
    low = i2c.readfrom_mem(address, addr + 1, 1)[0]
    value = high << 8 | low
    if value > 32768:
        value = value - 65536
    return value

def get_mpu6050_data(i2c):
    accel_x = (read_raw_data(i2c, ACCEL_XOUT_H) / 16384.0) - 0.006057997
    accel_y = (read_raw_data(i2c, ACCEL_XOUT_H + 2) / 16384.0) - 0.01469399
    accel_z = (read_raw_data(i2c, ACCEL_XOUT_H + 4) / 16384.0) +  -0.04595397
    gyro_x = read_raw_data(i2c, GYRO_XOUT_H) / 131.0
    gyro_y = read_raw_data(i2c, GYRO_XOUT_H + 2) / 131.0
    gyro_z = read_raw_data(i2c, GYRO_XOUT_H + 4) / 131.0

    return {
        'accel': {
            'x': round(accel_x, 2),
            'y': round(accel_y, 2),
            'z': round(accel_z, 2)
        },
        'gyro': {
            'x': round(gyro_x, 2),
            'y': round(gyro_y, 2),
            'z': round(gyro_z, 2),
        }
    }


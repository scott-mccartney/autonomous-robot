#!/usr/bin/python

import smbus
import math

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
	return bus.read_byte_data(address, adr)

def read_word(adr):
	high = bus.read_byte_data(address, adr)
	low = bus.read_byte_data(address, adr+1)
        val = (high << 8) + low
	return val

def read_word_2c(adr):
	val = read_word(adr)
	if(val >= 0x8000):
		return -((65535 - val) + 1)
	else:
		return val

def dist(a,b):
	return math.sqrt((a*a) + (b*b))

def get_y_rotation(x,y,z):
	radians = mat.atan2(x, dist(y, z))
	return -math.degress(radians)

def get_x_rotation(x,y,z):
        radians = math.atan2(y, dist(x,z))
        return math.degrees(radians)

bus = smbus.SMBus(1)
address = 0x68

bus.write_byte_data(address, power_mgmt_1, 0)

print("gyro data")
print("---------")

gx = read_word_2c(0x43)
gy = read_word_2c(0x45)
gz = read_word_2c(0x47)

print("gx: ", gx, "  scaled: ", (gx / 131))
print("gy: ", gy, "  scaled: ", (gy / 131))
print("gz: ", gz, "  scaled: ", (gz / 131))

print()
print("accelerometer data")
print("------------------")

ax = read_word_2c(0x3b)
ay = read_word_2c(0x3d)
az = read_word_2c(0x3f)

axs = ax / 16384.0
ays = ay / 16384.0
azs = az / 16384.0

print("ax: ", ax, "  scaled: ", axs)
print("ay: ", ay, "  scaled: ", ays)
print("az: ", az, "  scaled: ", azs)

print("x_rot: ", get_x_rotation(axs, ays, azs))
print("y_rot: ", get_y_rotation(axs, ays, azs))

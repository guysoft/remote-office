import serial
import time


ser = serial.Serial('/dev/ttyUSB0', 115200)
"""
time.sleep(2)
ser.write(str.encode("G28 x0 y0\n")) # Send to home
print("read:")
print(ser.readline())
# Set point to home
ser.write(str.encode("G92 x0 y0 z0\n"))
time.sleep(1)
ser.write(str.encode("G90\n")) # Use absulute coordinates
time.sleep(1)
print("read:")
print(ser.readline())
ser.write(str.encode("G01 x5 y5 f700\n")) # Go to location
time.sleep(1)
print("read:")
print(ser.readline())
print("read:")
print(ser.readline())
print(ser.readline())
time.sleep(1)
ser.write(str.encode("G92 x0 y0 z0\n"))
time.sleep(1)
print(ser.readline())
ser.write(str.encode("G1 x3 y6 z2\n"))
time.sleep(1)
print(ser.readline())
time.sleep(1)
ser.close()
"""

class GcodeController:
	def __init__(self):
		self.ser = serial.Serial('/dev/ttyUSB0', 115200)
		self.readline()
		self.readline()
		return
	def readline(self, debug="on"):
		return_value = self.ser.readline().strip()
		# if debug:
		# 	print(return_value)
		return return_value.decode()
	def __del__(self):
		self.ser.close()
		
	def send_command(self, command, debug="on"):
		self.ser.write(str.encode(command + "\n"))
		return_value = self.readline(debug="off")
		if debug:
			print(return_value)
		return return_value
		
	def send_to_home(self):
		print("send home")
		return self.send_command("G28 x0 y0")
	
	def send_use_absolute_coordinates(self):
		print("send use_absolute coordinates")
		return self.send_command("G90")
		
	def goto_location(self, x, y, speed="700"):
		print("Go to location: " + str(x) + "," + str(y) + " f" + str(speed))
		return self.send_command("G01 x" + str(x) + " y" + str(y) + " f" + str(speed))



if __name__ == "__main__":
	a = GcodeController()
	a.send_to_home()
	a.send_use_absolute_coordinates()
	a.goto_location(50, 50, 700)
	print("Done")

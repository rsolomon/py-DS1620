import RPi.GPIO as GPIO
import time

class DS1620:
"""
Instantiable class representing a DS1620 sensor.
Get the latest at:
https://github.com/rsolomon/py-DS1620

Ported from cypherkey's GPIO C# lib:
https://github.com/cypherkey/RaspberryPi.Net/blob/master/RaspberryPiDotNet/DS1620.cs
"""

	def __init__(self, rst, dq, clk):
		""" DS1620 sensor constructor.

		Keyword arguments:
		rst -- Integer corresponding to the RST GPIO Pin.
		dq  -- Integer DAT/DQ GPIO Pin.
		clk -- Integer CLK GPIO Pin.
		"""

		GPIO.setmode(GPIO.BCM)  # Set the mode to get pins by GPIO #
		self._rst = rst
		self._dq = dq
		self._clk = clk

	def __send_command(self, command):
		""" Sends an 8-bit command to the DS1620 """

		for n in range(0, 8):
			bit = ((command >> n) & (0x01))
			GPIO.output(self._dq, GPIO.HIGH if (bit == 1) else GPIO.LOW)
			GPIO.output(self._clk, GPIO.LOW)
			GPIO.output(self._clk, GPIO.HIGH)

	def __read_data(self):
		""" Read 8 bit data from the DS1620 """

		raw_data = 0  # Go into input mode.
		for n in range(0, 9):
			GPIO.output(self._clk, GPIO.LOW)
			GPIO.setup(self._dq, GPIO.IN)
			if GPIO.input(self._dq) == GPIO.HIGH:
				bit = 1
			else:
				bit = 0
			GPIO.setup(self._dq, GPIO.OUT)
			GPIO.output(self._clk, GPIO.HIGH)
			raw_data = raw_data | (bit << n)
		return raw_data

	def get_temperature(self):
		""" Send the commands to retrieve the temperature in Celsuis """

		# Prepare the pins for output.
		GPIO.setup(self._rst, GPIO.OUT)
		GPIO.setup(self._dq, GPIO.OUT)
		GPIO.setup(self._clk, GPIO.OUT)

		GPIO.output(self._rst, GPIO.LOW)
		GPIO.output(self._clk, GPIO.HIGH)
		GPIO.output(self._rst, GPIO.HIGH)
		self.__send_command(0x0c)  # Write config command.
		self.__send_command(0x02)  # CPU Mode.
		GPIO.output(self._rst, GPIO.LOW)
		time.sleep(0.2)  # Wait until the config register is written.
		GPIO.output(self._clk, GPIO.HIGH)
		GPIO.output(self._rst, GPIO.HIGH)
		self.__send_command(0xEE)  # Start conversion.
		GPIO.output(self._rst, GPIO.LOW)
		time.sleep(0.2)
		GPIO.output(self._clk, GPIO.HIGH)
		GPIO.output(self._rst, GPIO.HIGH)
		self.__send_command(0xAA)
		raw_data = self.__read_data()
		GPIO.output(self._rst, GPIO.LOW)
		return raw_data / 2.0

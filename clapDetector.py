from gpiozero import Button
import time

class ClapDetector:
	""" 
	detects and filters digital signals from a GPIO pin
	
	Parameters
	--------
	input_pin: int
		The number of the GPIO pin to witch the digital output of the sound sensor is connected
	clap_distance_threshold: float, optional
		defines how close together individual claps can be detected, in seconds

	Methods
	-------
	register_listener(function)
		register a function that should be called whenever a clap is detected. The function will be called with the time of the clap event as input parameter.
	"""
	def __init__(self, input_pin, clap_distance_threshold=0.01):
		self._digital_noise_input = Button(input_pin, pull_up = False)
		self._clap_distance_threshold = clap_distance_threshold
		self._last_detected_clap = 0
		self._listeners = set()
		self._digital_noise_input.when_pressed = lambda: self._noise_detected(time.time())
	
	def _noise_detected(self, event_time):
		if event_time - self._last_detected_clap > self._clap_distance_threshold:
			self._last_detected_clap = event_time
			self._inform_listeners(event_time)

	#Registers a function as a listener. The function has to accept a time as an input
	def register_listener(self, function):
		self._listeners.add(function)

	def _inform_listeners(self, event_time):
		for function in self._listeners:
			function(event_time)

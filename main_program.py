import clapAnalyzer, clapDetector
import time
import os
import serial
import struct
import json

deviceAddress = '00:18:E5:04:1E:B6'

json_string = '{"0": "0", "1": "1", "2": "2"}' # this is the mapping of the clap sequences to the messages sent to the arduino. Can be changed during program execution.

os.system('sudo rfcomm bind /dev/rfcomm0 ' + deviceAddress) # use the rfcomm protocol to turn the bluetooth device into a virtual serial device.

ser = serial.Serial('/dev/rfcomm0', 9600) # open serial connection to bluetooth device

def sequence_to_msg(sequence_number):
	""" 
	converts the sequnce_number into a byte message according to the mapping json

	Parameters
	-------
	sequence_number: int

	Returns
	-------
	msg: bytes
	"""
	j = json.loads(json_string)
	number = int(j[str(sequence_number)])
	msg = struct.pack("B", number)
	return msg

def pattern_detected(sequence_number):
	""" 
	sends the corresponding message to the bluetooth device
	
	Parameters
	-------
	sequence_number: int
	"""
	print('clap sequence {0} detected'.format(sequence_number))
	msg = sequence_to_msg(sequence_number)
	print(msg)
	ser.write(msg)

def clap_detected():
	print('clap detected')

# creat a clapDetector instance listening on GPIO21
detector = clapDetector.ClapDetector(21)
detector.register_listener(lambda x: clap_detected())
# create one ClapAnalyzer per pattern
analyzer0 = clapAnalyzer.ClapAnalyzer([0.25, 0.25, 0.5, 0.5])
analyzer1 = clapAnalyzer.ClapAnalyzer([0.5, 0.25, 0.25, 0.5])
analyzer2 = clapAnalyzer.ClapAnalyzer([0.5, 0.5, 0.25, 0.25])
# hook up the ClapAnalyzers to the ClapDetector
detector.register_listener(analyzer0.clap)
detector.register_listener(analyzer1.clap)
detector.register_listener(analyzer2.clap)
# hook up the pattern_detected function to the ClapAnalyzers
analyzer0.on_clap_sequence(lambda: pattern_detected(0))
analyzer1.on_clap_sequence(lambda: pattern_detected(1))
analyzer2.on_clap_sequence(lambda: pattern_detected(2))

# endless loop
try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	print('end program')
finally:
	ser.close()

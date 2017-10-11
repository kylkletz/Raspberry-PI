import RPi.GPIO as GPIO
from time import sleep
import os
import glob


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

def start():
	temperature_folder()
	setvalues()
	mainloop()
	
##Routes to the folder that the temperature sensor is saving to
def temperature_folder():
	base_dir = '/sys/bus/w1/devices/'
	device_folder = glob.glob(base_dir + '28*')
	##print (device_folder)
	device_file = device_folder[0] + '/w1_slave'

##Reads in the temperature folder
def raw_temp():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

##Extracts the temperature values from the file given
def temp_read():
    lines = raw_temp()
    while lines[0].strip()[-3:] != 'YES':
        sleep(.2)
        lines = raw_temp()
    temp_output = lines[1].find('t=')
    if temp_output != 1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 +32
        return temp_c, temp_f

		
def setvalues():
	##the GPIO pins that the sensors are connected to
	templight = 12
	temppin = 4
	##the initial duty cycle of the LED
	powerlevel = 0


def pinsetup():
	GPIO.setup(templight, GPIO.OUT)
	GPIO.setup(temppin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.output(templight, False)

## start the duty cycle for the intended pin (pwmpin)
def setPWM():
	power = GPIO.PWM(templight, 100)
	power.start(powerlevel)

def mainloop():
	while True:
		temp_c, temp_f = temp_read()
		if(temp_f <= 76):
			powerlevel = 0
		elif(temp_f >= 86):
			powerlevel = 100
		else:
			powerlevel = (temp_f -76)*10
		power.ChangeDutyCycle(powerlevel)
		
		print(temp_f)
    

	
	
start()
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def setup():
	sleepTime =.01
	##Assigning the GPIO pins to a variable for readability
	lightpin = 13
	buttonpin = 18
	pwmpin = 23
	changepin = 26
	##The while loop conditional
	keepgoing = True
	## Initial blinking speed for the light 1/tempo
	tempo = 2
	## The blinking speed is increasing conditional
	increasing = True
	##The initial duty cycle for the intensity of the second light
	powerlevel = 5
	##this boolean conrols the initial buttons functionality
	##when True the button pauses the incrementing of tempo
	##when False the button changes the intensity of the second light
	rotato = True
	setpins()
	setPWM()

def setpins():
	##initiate each GPIO pin for its intended functionality
	GPIO.setup(lightpin, GPIO.OUT)
	GPIO.setup(pwmpin, GPIO.OUT)
	GPIO.setup(buttonpin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(changepin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	##Set the lights to being off
	GPIO.output(lightpin, False)
	GPIO.output(pwmpin, False)
	
## start the duty cycle for the intended pin (pwmpin)
def setPWM():
	power = GPIO.PWM(pwmpin,100)
	power.start(powerlevel)	
	
##Swap the functionality of the first button
def swapping():
	print("swapping")
	if(rotato == True):
		rotato = False
	else:
		rotato = True
			
## Turns the lights on and off simulating blinking
def lightblink():
	GPIO.output(lightpin, True)
	GPIO.output(pwmpin, True)
	sleep(1/tempo)            
	GPIO.output(lightpin, False)
	GPIO.output(pwmpin,False)
	sleep(1/tempo)
		
##increases the tempo of the blinking up to 6 then resets to 2
def increasetempo():
	if(increasing):
		if(tempo < 6):
			tempo = tempo + .5       
		else:
			tempo = 2
			
##increases the intensity of the pwmpin
##starts at 5 duty cycle increasing by 20, up to 4 times then resetting to 5
def changeintensity():
	power.ChangeDutyCycle(powerlevel)
	if(GPIO.input(buttonpin) == False):
		powerlevel = powerlevel + 20
		if(powerlevel >85):
			powerlevel = 5

##Flips the increasing intensity on and off based on button pushes			
def istempoincreasing():
	if (GPIO.input(buttonpin) == False):
		print ("pressed?")
		if(increasing == True):
			increasing = False
		else:
			increasing = True
			
##Flips the function of the first button
##whether it affects the tempo or the intensity
def buttonfunction():
	if (rotato):
		increasetempo()
	else:
		##print('rotato false')
		changeintensity()
			
def mainloop():
	try:
		while keepgoing:
			if(GPIO.input(changepin) == False):
				swapping()
			lightblink()
			buttonfunction()
			istempoincreasing()
			GPIO.output(lightpin, GPIO.input(buttonpin))
			sleep(sleepTime)
			
	finally:
		GPIO.output(lightpin, False)
		GPIO.cleanup()
		
def start():
	setup()
	mainloop()
	

start()
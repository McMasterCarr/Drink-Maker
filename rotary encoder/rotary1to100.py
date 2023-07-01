# Import the module
from pyky040 import pyky040
import RPi.GPIO as GPIO

SW_PIN = 6  # Switch pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define your callback
def my_callback(scale_position):
    print('Hello world! The scale position is {}'.format(scale_position))

def switch_callback():
    print('switch clicked')

# Init the encoder pins
my_encoder = pyky040.Encoder(CLK=22, DT=4, SW=6)
# Or the encoder as a device (must be installed on the system beforehand!)
# my_encoder = pyky040.Encoder(device='/dev/input/event0')

# Setup the options and callbacks (see documentation)
my_encoder.setup(scale_min=0, scale_max=100, step=1, chg_callback=my_callback)
my_encoder.setup(sw_callback=switch_callback)
# Launch the listener
my_encoder.watch()

# Main program loop
try:
    while True:
        # Check the state of the switch
        if GPIO.input(SW_PIN) == GPIO.LOW:
            print("Switch Pressed")
        
        # Do other tasks or actions based on the counter value
except KeyboardInterrupt:
    # Clean up GPIO on program exit
    GPIO.cleanup()
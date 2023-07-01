import RPi.GPIO as GPIO

# Pin Definitions
SW_PIN = 6  # Switch pin
DT_PIN = 4  # DT pin
CLK_PIN = 22  # CLK pin

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT_PIN, GPIO.IN)
GPIO.setup(CLK_PIN, GPIO.IN)

# Variables
counter = 0  # Encoder counter value
clk_state = GPIO.input(CLK_PIN)
dt_state = GPIO.input(DT_PIN)

# Callback function for CLK pin interrupt
def clk_callback(channel):
    global counter, clk_state, dt_state

    # Read the current states of CLK and DT pins
    clk_state_new = GPIO.input(CLK_PIN)
    dt_state_new = GPIO.input(DT_PIN)

    if clk_state_new != clk_state:
        # CLK pin has changed, check DT pin
        if dt_state_new != clk_state_new:
            # DT pin is different from CLK, clockwise rotation
            counter += 1
        else:
            # DT pin is the same as CLK, counter-clockwise rotation
            counter -= 1

    # Update the states for the next interrupt
    clk_state = clk_state_new
    dt_state = dt_state_new

# Interrupt event detection for CLK pin falling edge
GPIO.add_event_detect(CLK_PIN, GPIO.FALLING, callback=clk_callback, bouncetime=10)

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

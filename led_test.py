import RPi.GPIO as GPIO
import time

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set up the GPIO pin for the LED
LED_PIN = 26  # Change this to your GPIO pin number
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        # Turn on the LED
        GPIO.output(LED_PIN, True)
        time.sleep(1)  # Wait for 1 second

        # Turn off the LED
        GPIO.output(LED_PIN, False)
        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    # Clean up the GPIO pins before exiting
    GPIO.cleanup()

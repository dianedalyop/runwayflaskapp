import RPi.GPIO as GPIO
import time

# GPIO pin setup HCRSO4
TRIG = 17  # Trigger Pin
ECHO = 18  # Echo Pin
LED = 23   # LED Pin


GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

# Function to measure distance
def measure_distance():
    # Send a pulse to the trigger pin
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    # Measure time for echo to return
    while GPIO.input(ECHO) == GPIO.LOW:
        pulse_start = time.time()
    while GPIO.input(ECHO) == GPIO.HIGH:
        pulse_end = time.time()

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Convert time to cm
    return round(distance, 2)

try:
    while True:
        distance = measure_distance()
        print(f"Distance: {distance} cm")
        
        
        if distance <= 10:
            print("Object detected! Blinking LED...")
            for _ in range(5):  # Blink LED 5 times
                GPIO.output(LED, GPIO.HIGH)  # Turn LED on
                time.sleep(0.2)  # Wait for 0.2 seconds
                GPIO.output(LED, GPIO.LOW)  # Turn LED off
                time.sleep(0.2)  # Wait for 0.2 seconds
        else:
            GPIO.output(LED, GPIO.LOW)  # Ensure LED is off
        time.sleep(1)  # Wait before measuring again

except KeyboardInterrupt:
    print("PROGRAM TERMINATED.")

finally:
    GPIO.cleanup()  # Clean up GPIO 

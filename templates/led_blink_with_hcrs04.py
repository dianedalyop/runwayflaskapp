import RPi.GPIO as GPIO
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback

# GPIO pin setup
TRIG = 17
ECHO = 18
LED = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

# PubNub configuration
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-cf192832-cac4-4813-a037-6ba18e798dcd"
pnconfig.publish_key = "pub-c-75f67faf-dd39-4f1c-9d61-c252d6b322e8"
pnconfig.uuid = "raspberry-pi-flight-uuid"
pubnub = PubNub(pnconfig)


def measure_distance():
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    while GPIO.input(ECHO) == GPIO.LOW:
        pulse_start = time.time()
    while GPIO.input(ECHO) == GPIO.HIGH:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

try:
    while True:
        distance = measure_distance()
        print(f"Distance: {distance} cm")

        if distance <= 10:
            message = {"status": "Object detected!", "distance": distance}
            pubnub.publish().channel("flight-channel").message(message).sync()
            print("Message published to PubNub.")
            GPIO.output(LED, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED, GPIO.LOW)
        else:
            GPIO.output(LED, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    print("PROGRAM TERMINATED.")
finally:
    GPIO.cleanup()

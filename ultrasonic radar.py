import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
from gpiozero import Servo
import math


TRIGGER_PIN = 23
ECHO_PIN = 24


SERVO_PIN = 17
servo = Servo(SERVO_PIN)


GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)



def measure_distance():
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound in cm/s
    return distance



def sweep_and_detect():
    angles = list(range(-90, 91, 10))
    distances = []

    for angle in angles:
        servo.value = angle / 90.0
        time.sleep(0.5)

        distance = measure_distance()
        distances.append(distance)

        # Plot objects
        plt.plot([0, distance * math.cos(math.radians(angle))],
                 [0, distance * math.sin(math.radians(angle))], marker='o')
        plt.xlim(0, 200)
        plt.ylim(-100, 100)
        plt.draw()
        plt.pause(0.1)

    servo.value = None
    return distances


if __name__ == "__main__":
    try:
        plt.ion()
        plt.figure()
        while True:
            distances = sweep_and_detect()
            print("Distances:", distances)

    except KeyboardInterrupt:
        pass

    finally:
        plt.ioff()
        GPIO.cleanup()

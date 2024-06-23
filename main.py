import time
import machine
from WeatherStationController import *

time.sleep(0.1)
print("Hello, Pi Pico!")

# Initialize the Miniweatherstation
myclock = WeatherStationController()
myclock.run()
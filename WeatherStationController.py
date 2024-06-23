# Import necessary libraries
import time
import random
from StateModel import *
from Button import *
from Clock import *
from Counters import *
from Displays import *
from Buzzer import *
from Lights import *
import dht
from Log import *

class WeatherStationController:

    def __init__(self):
        self._clock = Clock()
        self._display = LCDDisplay(sda=0, scl=1, i2cid=0)
        self._buttons = [
            Button(10, 'white', buttonhandler=None),
            Button(11, 'red', buttonhandler=None),
            Button(12, 'yellow', buttonhandler=None),
            Button(13, 'blue', buttonhandler=None)
        ]
        self.sensor1 = dht.DHT22(Pin(16))
        self.sensor2 = dht.DHT22(Pin(18))
        self.buzzer = Buzzer(Pin(17))
        self.led = Light(Pin(15))
        self._timer = SoftwareTimer(None)
        self._tempstatus = 0  # 0 for indoor, 1 for outdoor

        self._model = StateModel(10, self, debug=True)

        self._model.addButton(self._buttons[0])
        self._model.addButton(self._buttons[1])
        self._model.addButton(self._buttons[2])
        self._model.addButton(self._buttons[3])

        self._model.addTimer(self._timer)

        self._model.addTransition(0, [BTN1_PRESS], 1)
        self._model.addTransition(1, [BTN4_PRESS], 0)
        self._model.addTransition(1, [BTN2_PRESS], 2)
        self._model.addTransition(1, [BTN3_PRESS], 3)
        self._model.addTransition(2, [NO_EVENT], 1)
        self._model.addTransition(3, [NO_EVENT], 1)
        self._model.addTransition(1, [BTN1_PRESS], 4)
        self._model.addTransition(4, [BTN4_PRESS], 1)
        self._model.addTransition(4, [BTN2_PRESS], 5)
        self._model.addTransition(4, [BTN3_PRESS], 6)
        self._model.addTransition(5, [NO_EVENT], 4)
        self._model.addTransition(6, [NO_EVENT], 4)
        self._model.addTransition(9, [TIMEOUT], 0)

    def celsius_to_fahrenheit(self, celsius):
        return (celsius * 9/5) + 32

    def run(self):
        self._model.run()

    def stateDo(self, state):
        if state == 0:
            self.showTimeAndWeather()
            time.sleep(5)
        elif state == 1:
            self.showTime()
            time.sleep(1)
        elif state == 4:
            time.sleep(0.25)
        elif state == 5 or state == 6:
            time.sleep(0.25)
        elif state == 9:
            self.alertHighTemp()
            if self.checkTemperature() < 90:
                self._model.gotoState(0)
            time.sleep(1)

    def showTime(self):
        (_, _, _, hour, minute, _, _, _) = self._clock.getTime()
        formatted_time = f"Time: {hour:02}:{minute:02}"
        self._display.showText(f"{formatted_time:16.16}")

    def showTimeAndWeather(self):
        # Clear the display before showing new content
        self._display.clear()
        
        (_, _, _, hour, minute, _, _, _) = self._clock.getTime()
        formatted_time = f"Time: {hour:02}:{minute:02}"
        if self._tempstatus == 0:
            # Measure temperature and humidity for the first sensor (indoor)
            self.sensor1.measure()
            temp_in_c = self.sensor1.temperature()
            temp_in_f = self.celsius_to_fahrenheit(temp_in_c)
            humidity_in = self.sensor1.humidity()
            weather_data = f"In: {temp_in_f:.1f}F {humidity_in:.0f}%"
            # Display formatted time and weather data
            self._display.showText(f"{formatted_time:16.16}\n{weather_data:16.16}")
            self._tempstatus = 1
        else:
            # Measure temperature and humidity for the second sensor (outdoor)
            self.sensor2.measure()
            temp_in_c = self.sensor2.temperature()
            temp_in_f = self.celsius_to_fahrenheit(temp_in_c)
            humidity_out = self.sensor2.humidity()
            weather_data = f"Out: {temp_in_f:.1f}F {humidity_out:.0f}%"
            # Display formatted time and weather data
            self._display.showText(f"{formatted_time:16.16}\n{weather_data:16.16}")
            self._tempstatus = 0

    def stateEntered(self, state, event):
        if state == 0:
            Log.d('State 0 entered')
        elif state == 1:
            Log.d('State 1 entered')
            self._display.showText('Adjust hour ', 1, 0)
        elif state == 2:
            # Increment hour by 1
            self._clock.setHour((self._clock.getHour() + 1) % 24)
        elif state == 3:
            # Decrement hour by 1, wrap around if necessary
            new_hour = self._clock.getHour() - 1
            if new_hour < 0:
                new_hour = 23
            self._clock.setHour(new_hour)
        elif state == 4:
            Log.d('State 4 entered')
            self._display.showText('Adjust minute ', 1, 0)
        elif state == 5:
            self.adjustMinute(increment=True)
        elif state == 6:
            self.adjustMinute(increment=False)
        elif state == 9:
            Log.d('Alert state entered')
            # Set the alert timer to 10 seconds
            self._timer.set(10)

    def stateLeft(self, state, event):
        if state == 9:
            # Turn off the buzzer and LED when leaving the alert state
            self.buzzer.off()
            self.led.off()

    def adjustHour(self, increment=True):
        current_hour = self._clock.getHour()
        new_hour = (current_hour + (1 if increment else -1)) % 24
        self._clock.setHour(new_hour)

    def adjustMinute(self, increment=True):
        current_minute = self._clock.getMinute()
        new_minute = (current_minute + (1 if increment else -1)) % 60
        self._clock.setMinute(new_minute)
        self.showTime()  # Update the display immediately
        self._model.processEvent(NO_EVENT)  # Return to state 4

    def alertHighTemp(self):
        self.buzzer.beep()
        self.led.blink()

if __name__ == '__main__':
    WeatherStationController().run()

import enum
import threading
import time
from functools import partial
from threading import Thread


class SimpleHeater:
    def on(self):
        print("Heater is on")

    def off(self):
        print("Heater is off")


class SimpleCooler:
    def on(self):
        print("Cooler is on")

    def off(self):
        print("Cooler is off")


class SmartHeater(Thread):
    def __init__(self, airco):
        super().__init__()
        self._airco = airco
        self._running = False

    def on(self):
        print("Smart heater is on")
        self._running = True

    def off(self):
        print("Smart heater is off")
        self._running = False

    def run(self):
        while self._running and not self.airco._stop_event.is_set():
            t = self._airco.temp
            print(f"Heating: temperature = {t}")
            self._airco.temp = t + 0.2


class SmartCooler(Thread):
    def __init__(self, airco):
        super().__init__()
        self._airco = airco
        self._running = False

    def on(self):
        print("Smart cooler is on")
        self._running = True

    def off(self):
        print("Smart cooler is off")
        self._running = False

    def run(self):
        while self._running and not self.airco._stop_event.is_set():
            t = self._airco.temp
            print(f"Cooling: temperature = {t}")
            self._airco.temp = t - 0.2


class AircoState(enum.Enum):
    OK = 0
    COLD = -1
    WARM = +1


class Airco(Thread):
    def __init__(self, low_temp=19.0, high_temp=21.0):
        super().__init__()
        self.low_temp = low_temp
        self.high_temp = high_temp
        self._temperature = (low_temp + high_temp) / 2.0
        self._temperature_state = AircoState.OK
        self.heater = None
        self.cooler = None
        self._running = False
        self._stop_event = threading.Event()

    def on(self):
        self._running = True

    def off(self):
        self._cooling(False)
        self._heating(False)
        self._running = False

    @property
    def temp(self):
        return self._temperature

    @temp.setter
    def temp(self, value):
        self._temperature = value
        if value <= self.low_temp:
            self._temperature_state = AircoState.COLD
        elif value > self.high_temp:
            self._temperature_state = AircoState.WARM
        else:
            self._temperature_state = AircoState.OK

    def _cooling(self, value):
        if self.cooler is not None:
            self.cooler.on() if value else self.cooler.off()
        else:
            print("No cooler connected")

    def _heating(self, value):
        if self.heater is not None:
            self.heater.on() if value else self.heater.off()
        else:
            print("No heater connected")

    def run(self):
        actions = {
            AircoState.OK: (partial(self._heating, False), partial(self._cooling, False)),
            AircoState.COLD: (partial(self._heating, True), partial(self._cooling, False)),
            AircoState.WARM: (partial(self._heating, False), partial(self._cooling, True)),
        }
        previous_state = self._temperature_state
        while self._running and not self._stop_event.is_set():
            if self._temperature_state != previous_state:
                for action in actions[self._temperature_state]:
                    action()
            previous_state = self._temperature_state
            time.sleep(1)

    def stop(self):
        self._stop_event.set()

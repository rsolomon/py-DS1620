DS1620.py
=====================
A python port of cypherkey's RaspberryPi.Net DS1620 wrapper. Their wrapper can be found here:
https://github.com/cypherkey/RaspberryPi.Net

version
---------------------
0.0.1

usage
--------------------
```python
import RPi.GPIO as GPIO
from DS1620 import DS1620

GPIO.cleanup()
t_sensor = DS1620(17, 18, 27)
t_sensor.get_temperature()
```

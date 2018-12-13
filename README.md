# LED Worm Overview

![led-worm2](https://github.com/mresrever/led-worm/blob/master/led_worm.gif)

The worm that lives in 8*8 LED matrix :bug:

# Devices

- LED matrix(8*8): 1588BS
- Arduino-compatible hardware: Osoyoo Mega2560

![led-worm1](https://github.com/mresrever/led-worm/blob/master/led_worm.jpg)

# System

Python script ("led_worm.py") generates the animations (Sequencial 2d matrices) and send to the Arduino device with serial communication.
And the LED matrix is controlled by the Arduino device which runs "sketch_led_worm.ino".

# Misc

It isn't mandatory to control by python script because the animation can also be generated from Arduino sketch. However, it would be better to support the control by python script for the scalability. (Python is more flexible than Arduino sketch.)


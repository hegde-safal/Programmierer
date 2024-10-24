import time
import board
import adafruit_tcs34725

i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)
sensor.integration_time = 0xEB
sensor.gain = 0x01

def classify_apple_color(r, g, b):
    if r > 200 and g > 100 and b < 80:
        return "Ripe"
    elif r < 100 and g < 50 and b < 50:
        return "Rotten"
    else:
        return "Uncertain"

def detect_apples():
    while True:
        r, g, b = sensor.color_rgb_bytes
        classification = classify_apple_color(r, g, b)
        print(f"Apple color: R={r}, G={g}, B={b}, Classification: {classification}")
        time.sleep(1)

if _name_ == "_main_":
    try:
        detect_apples()
    except KeyboardInterrupt:
        print("Program interrupted.")
import time
from machine import Pin
from pimoroni import Analog, AnalogMux, Button
from servo import servo2040

# This Micropython code is loaded on the servo2040 driver board which waits for a
# voltage signal from the brain and will execute a function based on what voltage it receives

# Set up the shared analog inputs
sen_adc = Analog(servo2040.SHARED_ADC)
vol_adc = Analog(servo2040.SHARED_ADC, servo2040.VOLTAGE_GAIN)
cur_adc = Analog(servo2040.SHARED_ADC, servo2040.CURRENT_GAIN,
                 servo2040.SHUNT_RESISTOR, servo2040.CURRENT_OFFSET)

# Set up the analog multiplexer, including the pin for controlling pull-up/pull-down
mux = AnalogMux(servo2040.ADC_ADDR_0, servo2040.ADC_ADDR_1, servo2040.ADC_ADDR_2,
                muxed_pin=Pin(servo2040.SHARED_ADC))

# Set up the sensor addresses and have them pulled down by default
sensor_addrs = list(range(servo2040.SENSOR_1_ADDR, servo2040.SENSOR_6_ADDR + 1))
for addr in sensor_addrs:
    mux.configure_pull(addr, Pin.PULL_DOWN)

# Create the user button
user_sw = Button(servo2040.USER_SW)

# Create a list of servos for pins 0 to 7. Up to 16 servos can be created
START_PIN = servo2040.SERVO_1
END_PIN = servo2040.SERVO_8
servos = [Servo(i) for i in range(START_PIN, END_PIN + 1)]


# Select the first sensor to read from
mux.select(sensor_addrs[0])
print("S", 1, " = ", round(sen_adc.read_voltage(), 3), sep="", end=", ")


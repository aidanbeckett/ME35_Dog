import time
from machine import Pin
import uasyncio as asyncio
import machine
from servo import servo2040
from pimoroni import Analog, AnalogMux, Button

#import walk function from external file on board. same for sit
sen_adc_walk = Analog(servo2040.SHARED_ADC)
sen_adc_sit = Analog(servo2040.SHARED_ADC)
sen_adc_dance = Analog(servo2040.SHARED_ADC)

mux_walk = AnalogMux(servo2040.ADC_ADDR_0, servo2040.ADC_ADDR_1, servo2040.ADC_ADDR_2, muxed_pin=machine.Pin(servo2040.SHARED_ADC))
mux_sit = AnalogMux(servo2040.ADC_ADDR_0, servo2040.ADC_ADDR_1, servo2040.ADC_ADDR_2, muxed_pin=machine.Pin(servo2040.SHARED_ADC))
mux_dance = AnalogMux(servo2040.ADC_ADDR_0, servo2040.ADC_ADDR_1, servo2040.ADC_ADDR_2, muxed_pin=machine.Pin(servo2040.SHARED_ADC))

# Set up the sensor addresses and have them pulled down by default
sensor_addrs = list(range(servo2040.SENSOR_1_ADDR, servo2040.SENSOR_6_ADDR + 1))
mux_walk.configure_pull(sensor_addrs[0], machine.Pin.PULL_DOWN)
mux_sit.configure_pull(sensor_addrs[1], machine.Pin.PULL_DOWN)
mux_dance.configure_pull(sensor_addrs[2], machine.Pin.PULL_DOWN)


# Read from RP2040
walk_input = sensor_addrs[0]
sit_input = sensor_addrs[1]
dance_input = sensor_addrs[2]

# Create a list of servos for pins 0 to 7. Up to 16 servos can be created
START_PIN = servo2040.SERVO_1
END_PIN = servo2040.SERVO_8
servos = [Servo(i) for i in range(START_PIN, END_PIN + 1)]
# Back right leg: Servo(0) for hip joint and Servo(1) for knee joint
# Front right leg: Servo(2) for hip joint and Servo(3) for knee joint
# Front left leg: Servo(4) for hip joint and Servo(5) for knee joint
# Back right leg: Servo(6) for hip joint and Servo(7) for knee joint

# Enable all servos (this puts them at the middle)
for s in servos:
    s.enable()
        
#Define angles for taking a step
cycle1 = [-39.4,-44.3,-48.2,-51.3,-53.8,-55.5,-56.1,-55.6,-54.6,-52.9,-50.5,-47.4,-43.9,-40.2,\
        -35.8,-30.9,-26.5,-22.2,-17.6,-12.6,-12.6,-13.3,-14,-14.8,-15.5,-16.2,-16.8,-17.5,-18.2,\
        -18.8,-19.5,-20.1,-20.7,-21.3,-21.9,-22.5,-23.1,-23.7,-24.3,-24.8,-25.4,-25.9,-26.4,-27,\
        -27.5,-28,-28.5,-29,-29.4,-29.9,-30.4,-30.8,-31.3,-31.7,-32.1,-32.5,-32.9,-33.3,-33.7,-34.1,\
        -34.4,-34.8,-35.2,-35.5,-35.8,-36.1,-36.4,-36.7,-37,-37.3,-37.6,-37.8,-38.1,-38.3,-38.5,-38.7,\
        -38.9,-39.1,-39.3,-39.4]
cycle2 = [45.6,53.5,60.3,66,71.3,76.3,80.1,82.4,84.2,85.1,85,83.8,81.8,79.3,75.3,70,64.6,58.6,51.6,\
        43.4,43.4,44,44.5,44.9,45.4,45.8,46.2,46.6,47,47.4,47.7,48.1,48.4,48.7,49,49.2,49.5,49.7,49.9,\
        50.1,50.3,50.5,50.6,50.8,50.9,51,51.1,51.2,51.2,51.3,51.3,51.3,51.3,51.3,51.3,51.2,51.2,51.1,51,\
        50.9,50.8,50.7,50.6,50.4,50.2,50,49.8,49.6,49.4,49.1,48.8,48.5,48.2,47.9,47.6,47.2,46.9,46.5,\
        46.1,45.6]

def get_angle(curr,joint,shift):
    # If joint = 0 the motor is a hip joint, if 1 it is a knee joint
    # Shift is dependent on which leg the motor is on
    l = len(cycle1)
    phase_shift = l/4*shift
    if joint == 0:
        return cycle1[(curr+phase_shift)%l]
    else:
        return cycle2[(curr+phase_shift)%l]
        
def walk():
    count = 0
    while count < 2:
        # Loop through each angle value
        for i in range(len(cycle1)):
            time.sleep(0.05)
            # Set each servo to an angle in the series
            for j in range(0,4):
                # Each servo gets an angle based on which joint and leg it is on
                Servo(j).value(get_angle(i,i%2,round(j/2-0.25)))
            for j in range(4,8):
                # Angles for servos on the left side of the dog are negative because the servos are
                # oriented in the opposite direction
                Servo(j).value(-get_angle(i,i%2,round(j/2-0.25)))
        count+=1

def sit_execute():
    
    # Move legs to sitting position
    Servo(0).value(75)
    Servo(6).value(-75)
    Servo(1).value(-75)
    Servo(7).value(75)
    Servo(2).value(0)
    Servo(3).value(0)
    Servo(4).value(0)
    Servo(5).value(0)
# TODO: For all async checking loops: make so that current command is checked against
# previous command, if same commands, dont run, if not, run and update previous command
# to current command.
async def walking():
    mux_walk.select(walk_input)

    while True:
        sensor_1_reading = round(sen_adc_walk.read_voltage(), 3)
        if(sensor_1_reading > 2.5):
            walk()
            print("Should Walk")
        await asyncio.sleep(0.1)

async def sit():
    mux_sit.select(sit_input)
    
    while True:
        # sit (analog write)
        sensor_2_reading = round(sen_adc_sit.read_voltage(), 3)
        if(sensor_2_reading > 2.5):
            #execute sit function
            sit_execute()
            print("Should sit")
        await asyncio.sleep(0.1)

#TODO: Add global variable to check for start command. Update loops to not run until
# global is set

# async def toggle_activate():
#     while True:
#         await asyncio.sleep(0.1)

async def dance():
    mux_dance.select(dance_input)

    while True:
        # dance (analog write)
        sensor_3_reading = round(sen_adc_dance.read_voltage(), 3)
        if(sensor_3_reading > 2.5):
            #execute dance function
            dance_execute()
            print("Should dance")
        await asyncio.sleep(0.1)

def dance_execute():
    # Add dancing script here :)
    print("I like to move it move it")

async def main(duration):
    movement_task = asyncio.create_task(walking())
    sitting_task = asyncio.create_task(sit())
    dancing_task = asyncio.create_task(dance())

    await asyncio.sleep(duration)

def test(duration):
    try:
        asyncio.run(main(duration))
    except KeyboardInterrupt:
        print("Stopped")


test(10)

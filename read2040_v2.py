import time
from machine import Pin
import uasyncio as asyncio
import machine
from servo import servo2040
from pimoroni import Analog, AnalogMux, Button
from angles import cycle1, cycle2, dance1, dance2

#import walk function from external file on board. same for sit
sen_adc_walk = Analog(servo2040.SHARED_ADC)
sen_adc_sit = Analog(servo2040.SHARED_ADC)

mux_walk = AnalogMux(servo2040.ADC_ADDR_0, servo2040.ADC_ADDR_1, servo2040.ADC_ADDR_2, muxed_pin=machine.Pin(servo2040.SHARED_ADC))
mux_sit = AnalogMux(servo2040.ADC_ADDR_0, servo2040.ADC_ADDR_1, servo2040.ADC_ADDR_2, muxed_pin=machine.Pin(servo2040.SHARED_ADC))

# Set up the sensor addresses and have them pulled down by default
sensor_addrs = list(range(servo2040.SENSOR_1_ADDR, servo2040.SENSOR_6_ADDR + 1))
mux_walk.configure_pull(sensor_addrs[0], machine.Pin.PULL_DOWN)
mux_sit.configure_pull(sensor_addrs[1], machine.Pin.PULL_DOWN)


# Read from RP2040
walk_input = sensor_addrs[0]
sit_input = sensor_addrs[1]

# Create a list of servos for pins 0 to 7. Up to 16 servos can be created
START_PIN = servo2040.SERVO_1
END_PIN = servo2040.SERVO_8
servos = ServoCluster(pio=0, sm=0, pins=list(range(START_PIN, END_PIN + 1)))
# Back right leg: Servo(0) for hip joint and Servo(1) for knee joint
# Front right leg: Servo(2) for hip joint and Servo(3) for knee joint
# Front left leg: Servo(4) for hip joint and Servo(5) for knee joint
# Back right leg: Servo(6) for hip joint and Servo(7) for knee joint

def get_angle(curr,joint,shift):
    # If joint = 0 the motor is a hip joint, if 1 it is a knee joint
    # Shift is dependent on which leg the motor is on
    l = len(cycle1)
    phase_shift = int(len(cycle1)/4*shift)
    if joint == 0:
        return cycle1[(curr+phase_shift)%l]
    else:
        return cycle2[(curr+phase_shift)%l]
       
def dance_angle(curr,joint,shift):
    # If joint = 0 the motor is a hip joint, if 1 it is a knee joint
    # Shift is dependent on which leg the motor is on
    l = len(cycle1)
    phase_shift = int(len(cycle1)/4*shift)
    if joint == 0:
        return dance1[(curr+phase_shift)%l]
    else:
        return dance2[(curr+phase_shift)%l]
        
def walk():
    count = 0
    while count < 2:
        # Loop through each angle value
        for i in range(len(cycle1)):
            time.sleep(0.02)
            # Set each servo to an angle in the series
            for j in range(0,4):
                # Each servo gets an angle based on which joint and leg it is on
                servos.value(j, get_angle(i,j%2,round(j/2-0.25)), load=False)
            for j in range(4,8):
                # Angles for servos on the left side of the dog are negative because the servos are
                # oriented in the opposite direction
                servos.value(j, -get_angle(i,j%2,round(j/2-0.25)), load=False)
            servos.load()
        
        count+=1

def dance():
    count = 0
    while count < 3:
        # Loop through each angle value
        for i in range(len(dance1)):
            time.sleep(0.02)
            # Set each servo to an angle in the series
            for j in range(0,4):
                # Each servo gets an angle based on which joint and leg it is on
                servos.value(j, dance_angle(i,j%2,round(j/2-0.25)), load=False)
            for j in range(4,8):
                # Angles for servos on the left side of the dog are negative because the servos are
                # oriented in the opposite direction
                servos.value(j, -dance_angle(i,j%2,round(j/2-0.25)), load=False)
            servos.load()
        
        count+=1

def sit_execute():
    
    # Move legs to sitting position
    servos.value(0,75,load=False)
    servos.value(6,-75,load=False)
    servos.value(1,-75,load=False)
    servos.value(7,75,load=False)
    servos.value(2,0,load=False)
    servos.value(3,0,load=False)
    servos.value(4,0,load=False)
    servos.value(5,0,load=False)
    servos.load()

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

async def main(duration):
    movement_task = asyncio.create_task(walking())
    sitting_task = asyncio.create_task(sit())

    await asyncio.sleep(duration)

def test(duration):
    try:
        asyncio.run(main(duration))
    except KeyboardInterrupt:
        print("Stopped")


test(10)

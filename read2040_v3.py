import time
from machine import Pin
import uasyncio as asyncio
import machine
from servo import servo2040, ServoCluster
from pimoroni import Analog, AnalogMux, Button
from angles import cycle1, cycle2, dance1, dance2

# TODO: Compartmentalize pin setup to make code look cleaner.

#import walk function from external file on board. same for sit
sen_adc = Analog(servo2040.SHARED_ADC)

mux = AnalogMux(servo2040.ADC_ADDR_0, servo2040.ADC_ADDR_1, servo2040.ADC_ADDR_2, muxed_pin=machine.Pin(servo2040.SHARED_ADC))

# Set up the sensor addresses and have them pulled down by default
sensor_addrs = list(range(servo2040.SENSOR_1_ADDR, servo2040.SENSOR_6_ADDR + 1))
for address in sensor_addrs:
    mux.configure_pull(address, machine.Pin.PULL_DOWN)

# Read from RP2040
walk_input = sensor_addrs[0]
sit_input = sensor_addrs[1]
dance_input = sensor_addrs[2]
start_input = sensor_addrs[3]
turnhead_input = sensor_addrs[5]

# Create a list of servos for pins 0 to 7. Up to 16 servos can be created
START_PIN = servo2040.SERVO_1
END_PIN = servo2040.SERVO_12
servos = ServoCluster(pio=0, sm=0, pins=list(range(START_PIN, END_PIN + 1)))
# Back right leg: Servo(0) for hip joint and Servo(1) for knee joint
# Front right leg: Servo(2) for hip joint and Servo(3) for knee joint
# Front left leg: Servo(4) for hip joint and Servo(5) for knee joint
# Back right leg: Servo(6) for hip joint and Servo(7) for knee joint

allowReading = False
previousCommand = ""

# TODO: Broken rn. 
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
    while count < 2: #How many step cycles it will take per function call
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
        
def dance_execute():
    print("I like to move it move it")
    count = 0
    while count < 3: #How many step cycles it will take per function call
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

    servos.value(0,-65,load=False)
    servos.value(6,65,load=False)
    servos.value(1,75,load=False)
    servos.value(7,-75,load=False)
    servos.value(2,-65,load=False)
    servos.value(3,75,load=False)
    servos.value(4,65,load=False)
    servos.value(5,-75,load=False)
    servos.load()

async def walking():
    global allowReading
    global previousCommand

    while allowReading:
        mux.select(walk_input)
        sensor_1_reading = round(sen_adc.read_voltage(), 3)
        if(sensor_1_reading > 2.5 and previousCommand != "walk"):
            previousCommand = "walk"
            walk()
            print("Should Walk")
            previousCommand = ""
            wag_execute()
        await asyncio.sleep(0.1)

async def sit():
    global allowReading
    global previousCommand
    
    while allowReading:
        # sit (analog write)
        mux.select(sit_input)
        sensor_2_reading = round(sen_adc.read_voltage(), 3)
        if(sensor_2_reading > 2.5 and previousCommand != "sit"):
            #execute sit function
            previousCommand = "sit"
            sit_execute()
            print("Should sit")
            previousCommand = ""
            wag_execute()
        await asyncio.sleep(0.1)

async def toggle_activate():
    global allowReading
    global previousCommand

    while True:
        mux.select(start_input)
        sensor_4_reading = round(sen_adc.read_voltage(), 3)
        sensor_5_reading = round(sen_adc.read_voltage(),3)

        if(sensor_4_reading > 2.5 and previousCommand != "start"):
            allowReading = True
            previousCommand = "start"
            print("should start")
            wag_execute()
            break

    await asyncio.sleep(0.1)

async def dance():
    global allowReading
    global previousCommand

    while allowReading:
        # dance (analog write)
        mux.select(dance_input)
        sensor_3_reading = round(sen_adc.read_voltage(), 3)
        if(sensor_3_reading > 2.5 and previousCommand != "dance"):
            #execute dance function
            previousCommand = "dance"
            dance_execute()
            print("Should dance")
            previousCommand = ""
        await asyncio.sleep(0.1)

async def headPan():
    global allowReading
    global previousCommand

    while allowReading:
        # dance (analog write)
        mux.select(turnhead_input)
        sensor_6_reading = round(sen_adc.read_voltage(), 3)
        if(sensor_6_reading > 2.5 and previousCommand != "headPanLeft"):
            #execute dance function
            previousCommand = "headPanLeft"
            pan_left_execute()
            print("Should pan left")
        elif(sensor_6_reading > 2.5 and previousCommand != "headPanRight"):
            #execute dance function
            previousCommand = "headPanRight"
            pan_right_execute()
            print("Should pan right")
        await asyncio.sleep(0.1)

def wag_execute():
    print("Wag :)")
    for i in range(3):
        servos.value(8, -45)
        time.sleep(0.5)
        servos.value(8, 45)
        time.sleep(0.5)

def pan_left_execute():
    servos.value(10, -45)

def pan_right_execute():
    servos.value(10, 45)
    

async def main(duration):
    activation_task = asyncio.create_task(toggle_activate())
    movement_task = asyncio.create_task(walking())
    sitting_task = asyncio.create_task(sit())
    dancing_task = asyncio.create_task(dance())
    head_turn_task = asyncio.create_task(headPan())

    await asyncio.sleep(duration)

def test(duration):
    try:
        asyncio.run(main(duration))
    except KeyboardInterrupt:
        print("Stopped")


test(3000)

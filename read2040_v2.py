import time
from machine import Pin
import uasyncio as asyncio
import machine
from servo import servo2040
from pimoroni import Analog, AnalogMux, Button

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
servos = [Servo(i) for i in range(START_PIN, END_PIN + 1)]
# Back right leg: Servo(0) for hip joint and Servo(1) for knee joint
# Front right leg: Servo(2) for hip joint and Servo(3) for knee joint
# Front left leg: Servo(4) for hip joint and Servo(5) for knee joint
# Back right leg: Servo(6) for hip joint and Servo(7) for knee joint

# Enable all servos (this puts them at the middle)
for s in servos:
    s.enable()
        
#Define angles for taking a step
theta1 = [-64,-68,-71,-73,-75,-76,-76,-75,-74,-72,-68,-65,-61,-57,-52,-47,-43,-39,-36,-33]
theta2 = [-9,-4,1,5,9,13,16,18,20,21,21,20,18,16,12,8,4,-1,-5,-11]
    
#Define angles for pushing the grounded legs forward
drift1 = [-33,-35,-37,-39,-41,-43,-45,-47,-49,-51,-53,-54,-56,-57,-59,-60,-61,-62,-63,-64]
drift2 = [-11,-9,-9,-8,-7,-6,-6,-5,-5,-5,-5,-5,-5,-5,-6,-6,-7,-7,-8,-9]

def step(legs):
    # if legs = 0, the front left and back right move forward
    # if legs = 1 the front right and back left move forward
    
    # Loop through each angle value
    for i in range(len(theta1)):
        time.sleep(0.05)
        # Set each servo to an angle in the series
        for j in range(len(servos)):
            # Shift which servos are moving based on which legs are taking a step
            a = (j+(2*legs))%8
            if a%4 == 0:
                Servo(j).value(theta1[count])
            elif a%4 == 1:
                Servo(j).value(theta2[count])
            elif a%4 == 2:
                Servo(j).value(drift1[count])
            else:
                Servo(j).value(drift2[count])
        
def walk():
    
    # Move legs to starting position
    for i in range(len(servos)):
        if i%2==0:
            Servo[i].value(drift1[round(len(drift1)/2)])
        else:
            Servo[i].value(drift2[round(len(drift1)/2)])
     
    time.sleep(0.5)
    
    # Take first step
    for i in range(len(theta1)/2):
        count = i+len(theta1)/2
        time.sleep(0.05)
        for j in range(len(servos)):
            if j%4 == 0:
                Servo(j).value(theta1[count])
            elif j%4 == 1:
                Servo(j).value(theta2[count])
            elif j%4 == 2:
                Servo(j).value(drift1[count])
            else:
                Servo(j).value(drift2[count])
        
    listen(1)
    stepcount = 1
    
    # Alternate steps continuously while listening for new commands
    for i in range(4):
        step(stepcount%2)
        stepcount += 1

def sit_execute():
    
    # Move legs to sitting position
    Servo(0).value(75)
    Servo(6).value(75)
    Servo(1).value(-75)
    Servo(7).value(-75)
    Servo(2).value(0)
    Servo(3).value(0)
    Servo(4).value(0)
    Servo(5).value(0)

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

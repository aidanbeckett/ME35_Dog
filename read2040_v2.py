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

        
async def walking():
    mux_walk.select(walk_input)

    while True:
        sensor_1_reading = round(sen_adc_walk.read_voltage(), 3)
        if(sensor_1_reading > 2.5):
            #execute walk function
            print("Should Walk")
        await asyncio.sleep(0.1)

async def sit():
    mux_sit.select(sit_input)
    
    while True:
        # sit (analog write)
        sensor_2_reading = round(sen_adc_sit.read_voltage(), 3)
        if(sensor_2_reading > 2.5):
            #execute sit function
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

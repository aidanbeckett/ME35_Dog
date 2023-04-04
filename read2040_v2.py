import asyncio
import machine

#import walk function from external file on board. same for sit

# Read from RP2040
walk_input =  #Sensor 1
sit_input =  #Sensor 2

reading = 0

WALKING = 0
SIT = 0

        
async def walking():
    sensor_1_reading = 

    while True:
        if(sensor_1_reading > 2.5):
            #execute walk function
            walk()
        await asyncio.sleep(0.1)

async def sit():
    sensor_2_reading = 
    
    while True:
        # sit (analog write)
        if(sensor_2_reading > 2.5):
            #execute sit function
            sittingFunction()
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

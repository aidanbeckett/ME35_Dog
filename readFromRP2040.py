import asyncio
import machine

#import walk function from external file on board. same for sit

# Read from RP2040
analogInput = machine.Pin(27, machine.Pin.IN)

reading = 0

WALKING = 0
SIT = 0

async def read_2040():
    global reading

    while True:
        #read camera
        reading = analogInput.read()
        await asyncio.sleep(0.1)
        
async def walking():
    global reading

    while True:
        if(reading == WALKING):
            #execute walk function
            walk()
        await asyncio.sleep(0.1)

async def sit():
    global reading
    
    while True:
        # sit (analog write)
        if(reading == SIT):
            #execute sit function
            sittingFunction()
        await asyncio.sleep(0.1)

async def main(duration):
    rp2040_task = asyncio.create_task(read_2040())
    movement_task = asyncio.create_task(walking())
    sitting_task = asyncio.create_task(sit())

    await asyncio.sleep(duration)

def test(duration):
    try:
        asyncio.run(main(duration))
    except KeyboardInterrupt:
        print("Stopped")


test(10)
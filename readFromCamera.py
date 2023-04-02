import asyncio
import machine

# Send out to External RP2040
analogOutput = machine.Pin(26, machine.Pin.OUT)

# Read from Camera
analogInput = machine.Pin(27, machine.Pin.IN)

reading = 0

WALKING = 0
SIT = 0

async def read_camera():
    global reading

    while True:
        #read camera
        reading = analogInput.read()
        await asyncio.sleep(0.1)
        
async def walking():
    global reading

    while True:
        if(reading == WALKING):
            analogOutput.write(50)
        await asyncio.sleep(0.1)

async def sit():
    global reading
    
    while True:
        # sit (analog write)
        if(reading == SIT):
            analogOutput.write(100)
        await asyncio.sleep(0.1)

async def main(duration):
    camera_task = asyncio.create_task(read_camera())
    movement_task = asyncio.create_task(walking())
    sitting_task = asyncio.create_task(sit())

    await asyncio.sleep(duration)

def test(duration):
    try:
        asyncio.run(main(duration))
    except KeyboardInterrupt:
        print("Stopped")


test(10)
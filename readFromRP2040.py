import asyncio

async def read_2040():
    while True:
        #read 2040
        await asyncio.sleep(0.1)
        
async def walking():
    while True:
        #walk (analog write)
        await asyncio.sleep(0.1)

async def sit():
    while True:
        # sit (analow write)
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
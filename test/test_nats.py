import asyncio
import nats
import json

async def main():
    nc = await nats.connect("nats://localhost:4222")

    test_dict = {
        "coordinates": {
            "x": 0.965,
            "y": 1054.34,
            "rotate": 43.35
        },
        "velocity": {
            "x": 0.965,
            "y": 1054.34,
            "rotate": 43.35
        },
        "acceleration": {
            "x": 0.965,
            "y": 1054.34,
            "rotate": 43.35
        },
        "timestep": 0.001
    }

    payload = json.dumps(test_dict).encode()

    await nc.publish("ct.state", payload)

if __name__ == '__main__':
    asyncio.run(main())

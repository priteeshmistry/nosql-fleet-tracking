import paho.mqtt.client as mqtt
import time
import json
import random
import datetime

# connect to mqtt broker
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost", 1883, 60)
client.loop_start()

print("Simulator started. sending data...")

try:
    while True:
        # pick a random truck from 101 to 105
        t_id = random.randint(101, 105)
        truck_name = f"TRK-{t_id}"

        # create the json data
        data = {
            "vehicle_id": truck_name,
            "speed_kmh": random.randint(50, 90),
            "fuel_percent": round(random.uniform(10.0, 100.0), 1),
            "timestamp": str(datetime.datetime.now())
        }

        # send to the telemetry topic
        client.publish("fleet/telemetry/trucks", json.dumps(data))
        
        print("Sent:", data) # left this in for debugging
        time.sleep(2) 
        
except KeyboardInterrupt:
    print("\nStopped.")
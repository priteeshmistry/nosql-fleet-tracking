import paho.mqtt.client as mqtt
import time
import json
import random
import datetime

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost", 1883, 60)
client.loop_start()

print("Simulator started. Registering fleet in SQL...")


for t_id in range(101, 106):
    admin_data = {
        "vehicle_id": f"TRK-{t_id}",
        "license_plate": f"XYZ-910{t_id-100}",
        "status": "Active"
    }
    client.publish("fleet/admin/registry", json.dumps(admin_data))


time.sleep(2) 
print("Fleet registered. Sending live telemetry...")


cities_list = ["Messina", "Catania", "Palermo", "Rome", "Milan", "Naples"]

try:
    while True:
        t_id = random.randint(101, 105)
        
        data = {
            "vehicle_id": f"TRK-{t_id}",
            "speed_kmh": random.randint(50, 90),
            "fuel_percent": round(random.uniform(10.0, 100.0), 1),
            "location": random.choice(cities_list),
            "timestamp": str(datetime.datetime.now())
        }

        client.publish("fleet/telemetry/trucks", json.dumps(data))
        time.sleep(2) 
        
except KeyboardInterrupt:
    print("\nStopped.")
import paho.mqtt.client as mqtt
import json
import random
import mysql.connector
from pymongo import MongoClient
from py2neo import Graph

cities_list = ["Messina", "Catania", "Palermo", "Rome", "Milan", "Naples"]

# 1. Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password123",
    database="fleet_sql"
)
mycursor = mydb.cursor()
# make table if not exists
mycursor.execute("CREATE TABLE IF NOT EXISTS vehicles (vehicle_id VARCHAR(50) PRIMARY KEY, license_plate VARCHAR(50), status VARCHAR(50))")
mydb.commit()

# 2. Connect to MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mydb_mongo = mongo_client["fleet_database"]
mycol = mydb_mongo["telemetry"]

# 3. Connect to Neo4j
# Note: make sure to change your_password
graph_db = Graph("bolt://localhost:7687", auth=("neo4j", "your_password"))


def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected to MQTT with result code", rc)
    # subscribe to both topics
    client.subscribe("fleet/admin/registry")
    client.subscribe("fleet/telemetry/trucks")

def on_message(client, userdata, msg):
    payload_str = msg.payload.decode("utf-8")
    data = json.loads(payload_str)
    topic = msg.topic

    # print("Got message from:", topic)

    if topic == "fleet/admin/registry":
        v_id = data["vehicle_id"]
        plate = data["license_plate"]
        status = data["status"]

        # insert into sql, update if already there
        sql = "INSERT INTO vehicles (vehicle_id, license_plate, status) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE license_plate=VALUES(license_plate), status=VALUES(status)"
        val = (v_id, plate, status)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Saved to SQL:", v_id)

    elif topic == "fleet/telemetry/trucks":
        v_id = data["vehicle_id"]

        # save directly to mongo
        mycol.insert_one(data.copy())

        # pick random city and save to neo4j
        loc = random.choice(cities_list)
        
        # using f-string for the cypher query
        cypher_query = f"MERGE (v:Vehicle {{id: '{v_id}'}}) MERGE (c:City {{name: '{loc}'}}) MERGE (v)-[:VISITED]->(c)"
        graph_db.run(cypher_query)

        print(f"Saved {v_id} telemetry to Mongo and Neo4j (City: {loc})")


# start mqtt client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
print("Waiting for messages...")
client.loop_forever()
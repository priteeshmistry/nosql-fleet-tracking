# Fleet Tracking IoT System (DB-B2)

## Overview
This project is an integrated IoT system that collects, processes, and stores massive volumes of sensor data using an MQTT broker and Python. Data is dynamically routed to SQL, MongoDB, or Neo4j based on the MQTT topic.

## System Architecture
[IoT Simulator] 
      │ (JSON Payload via MQTT)
      ▼
[Mosquitto Broker] ──► Topic: fleet/admin/# ─────► [MySQL] (Static Registry)
      │
      └──────────────► Topic: fleet/telemetry/# ─┬─► [MongoDB] (Live Telemetry)
                                                 │
                                                 └─► [Neo4j] (Spatial Graph)

## Infrastructure Setup (Docker)
Ensure Docker is installed and run the following containers:

1. **Mosquitto MQTT Broker:**
   `docker run -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto`

2. **MySQL:**
   `docker run --name mysql_db -e MYSQL_ROOT_PASSWORD=password123 -p 3306:3306 -d mysql`

3. **MongoDB:**
   `docker run --name mongodb -p 27017:27017 -d mongo`

4. **Neo4j:**
   `docker run --name neo4j_db -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/your_password -d neo4j`

## Execution
1. Activate the Python virtual environment: `source venv/bin/activate`
2. Start the router: `python3 router.py`
3. Start the simulator: `python3 simulator.py`

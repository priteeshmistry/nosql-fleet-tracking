# Fleet Tracking Project

## Overview
This project simulates a high-velocity IoT fleet tracking system. It generates vehicle telemetry and administrative data, transmits it via an MQTT broker (Eclipse Mosquitto), and routes the data to three distinct database paradigms based on the MQTT message topic:

1. **MySQL (Relational):** Stores static vehicle registry data (Truck ID, License Plate).
2. **MongoDB (Document NoSQL):** Ingests high-velocity, unstructured JSON telemetry (speed, fuel, timestamps).
3. **Neo4j (Graph NoSQL):** Maps dynamic spatial relationships between vehicles and the cities they visit.

## Prerequisites
* Docker Desktop
* Python 3.x
* Required Python Libraries: `paho-mqtt`, `mysql-connector-python`, `pymongo`, `py2neo`

## 1. Infrastructure Setup (Docker)
Run these commands in your terminal to spin up the required database and broker containers.

**Start Mosquitto MQTT Broker:**
`docker run -d -p 1883:1883 --name mosquitto eclipse-mosquitto`

**Start MySQL Database:**
`docker run -d -p 3306:3306 --name mysql_db -e MYSQL_ROOT_PASSWORD=password123 -e MYSQL_DATABASE=fleet_sql mysql:latest`

**Start MongoDB:**
`docker run -d -p 27017:27017 --name mongodb mongo:latest`

**Start Neo4j:**
`docker run -d -p 7474:7474 -p 7687:7687 --name neo4j -e NEO4J_AUTH=neo4j/your_password neo4j:latest`

## 2. Execution
Start the routing engine first to ensure no MQTT messages are dropped, then start the IoT simulation.

1. **Start the Router:** Open a terminal and run `python3 router.py`.
2. **Start the Simulator:** Open a second terminal and run `python3 simulator.py`.

The simulator will begin publishing telemetry payloads to the `fleet/telemetry/trucks` topic, and the router will distribute the data across MongoDB and Neo4j automatically.

## 3. Data Verification
* **MySQL:** Run `python3 view_sql.py` to print the formatted registry table.
* **MongoDB:** Connect via MongoDB Compass to `mongodb://localhost:27017/` to view the telemetry documents.
* **Neo4j:** Navigate to `http://localhost:7474` and execute `MATCH (n) RETURN n` to view the spatial graph.

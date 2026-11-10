# Project explanation in plain English

This project is a training course about using artificial intelligence in industry.

It does not use a real factory. Instead, it simulates a production line in Docker containers. That means you can run the whole system locally on your computer and learn how industrial data and AI work together.

The project is built around a fake machining station called EST-01.

This station produces data such as:

- temperature
- vibration
- motor current
- cycle time
- piece ID and sequence number

The idea is to show how data moves inside an industrial system, how it is stored, how operators monitor it, and how AI can later use it to detect issues or predict failures.

## 1. What this project teaches

The project teaches a full pipeline:

1. A machine generates data
2. The data is sent through a message system
3. The data is stored in a database
4. Operators view it in a dashboard
5. Monitoring tools track it with alerts
6. AI models can later use it for prediction or quality decisions

This is the real thinking behind industrial AI: do not start with the model. Start with the data foundation.

## 2. The big picture

The course is organized in modules:

- M01: industrial architecture, monitoring, observability
- M02: capture and data integration
- M03: machine learning for prediction and anomaly detection
- M04: computer vision for quality inspection
- M05: generative AI and local language models
- M06: edge AI and industrial integration
- M07: operations, MLOps, and observability
- M08: cybersecurity and governance

The project is about showing how an industrial data architecture works before any AI model is added.

## 3. The main folders

The project has a few important sections:

- [README.md](./README.md) — course index
- [labs/](./labs/) — course theory and labs
- [infra/](./infra/) — all technical runtime files and Docker setup
- [infra/data/](./infra/data/) — live data and historical database
- [infra/linea/](./infra/linea/) — Python code for the simulated line
- [infra/prometheus/](./infra/prometheus/) — Prometheus config and alerts
- [infra/modelos/](./infra/modelos/) — local model files

## 4. What Docker is doing here

The most important file is [infra/docker-compose.yml](./infra/docker-compose.yml).

This file defines all the services that run together to simulate the line.

### Main services

- `mosquitto` — an MQTT broker, like a message bus
- `sensor` — generates machine data
- `archivador` — saves the data to SQLite
- `opcua` — exposes data through OPC UA industrial protocol
- `modbus` — exposes data through Modbus protocol
- `panel` — a dashboard for the operator
- `llm` — local AI model
- `api` — inference API
- `prometheus` — monitoring and alerting system
- `lab` — a runner for the exercises

This is not one program. It is a small ecosystem of services working together.

## 5. The base image

The file [infra/Dockerfile](./infra/Dockerfile) builds the runtime image for the project.

It installs:

- Python
- project dependencies
- the LLM runtime packages
- the local app code

This means every service runs on the same Python environment and uses the same codebase.

## 6. How the data flow works

The full path is:

1. A sensor makes values
2. It publishes them through MQTT
3. A database stores them
4. A dashboard shows them
5. Metrics and alerts monitor them
6. AI models can use them later

This is the real flow of industrial data.

## 7. Step by step: where the data comes from

The main machine logic is in [infra/linea/sensor.py](./infra/linea/sensor.py).

This script simulates a machining station and produces a result for each piece.

For each piece, it calculates values like:

- piece ID
- sequence number
- temperature
- vibration
- motor current
- cycle time
- timestamp

It then:

- stores the latest state in [infra/data/estado.json](./infra/data/estado.json)
- publishes the same data to MQTT
- exposes metrics to Prometheus

This is the origin of the system.

## 8. MQTT: the transport layer

MQTT is the message system used in this project.

A broker receives messages and sends them to all subscribers.

The project uses topics such as:

- `linea/est01/ciclo`
- `linea/est01/evento`
- `linea/est01/consigna`

The key point is that MQTT is fast and lightweight, but it is not a database.

It is just a transport layer. It distributes the data immediately, but it does not keep a long-term history by itself.

## 9. The historian: where the records are stored

The data is stored by [infra/linea/archivador.py](./infra/linea/archivador.py).

This service listens to MQTT and writes every production record into SQLite in [infra/data/historial.sqlite](./infra/data/historial.sqlite).

This gives the project a real historical record.

Without this storage layer, the data would exist only in a live stream and would be lost quickly.

## 10. The live state file

The sensor also writes the current machine state to [infra/data/estado.json](./infra/data/estado.json).

This is a current snapshot of the machine.

It is useful for:

- quick checking
- dashboards
- scripts and external services
- synchronization between components

## 11. Monitoring and alarm system

The observability layer is built from:

- [infra/linea/metricas.py](./infra/linea/metricas.py)
- [infra/prometheus/prometheus.yml](./infra/prometheus/prometheus.yml)
- [infra/prometheus/alertas.yml](./infra/prometheus/alertas.yml)

Prometheus pulls metrics from services, and alert rules tell the system when something is wrong.

This is a very important concept in industrial systems: sometimes a process is not “failed” in a strict sense, but it is performing badly and needs attention.

That is why the course teaches metrics and alerts before AI models.

## 12. Dashboards and supervision

The user-facing dashboard is in [infra/linea/panel.py](./infra/linea/panel.py).

It shows the production status and the values from the production data.

This is the part that the operator sees. It helps answer practical questions like:

- Is the machine healthy?
- Are the values stable?
- Are we seeing drift or abnormal behavior?
- Is the signal fresh enough to trust?

# 13. Lab validation: how the exercises check your work

The project uses commands in [infra/linea/cli.py](./infra/linea/cli.py).

This file contains validation logic for each lab. For example:

- `m01-01`
- `m01-02`
- `m02-01`
- `sql`
- `resumen`
- `notas`

These commands usually check whether the system is producing data, storing it correctly, and responding as expected.

If a command prints `OK`, the lab step is passing.

If it prints `FALLO`, then something is wrong in the pipeline.

This is how the project turns theory into practical verification.

## 14. Why this project is important

The most important lesson is this:

AI is not the first thing you build in an industrial environment.

Before you create a model, you need:

- correct data collection
- reliable timestamps
- stable transport
- storage
- monitoring
- clear dashboards
- defined alerting

If any of those are weak, your AI model will be weak too.

This project teaches the data and operational foundation before the advanced ML parts.

## 15. The simplest way to understand the project

If you want the shortest mental model, use this:

- Docker starts the environment
- Sensor generates live industrial data
- MQTT transports the live data
- Archivador stores it in SQLite
- Panel visualizes the state
- Prometheus monitors it with alerts
- Lab commands validate the setup
- Later modules add prediction, AI, and industrial integration

That is the whole story.

## 16. The main files to study first

If you are new to this project, read these first:

1. [README.md](./README.md)
2. [labs/comandos-lab.md](./labs/comandos-lab.md)
3. [infra/docker-compose.yml](./infra/docker-compose.yml)
4. [infra/Dockerfile](./infra/Dockerfile)
5. [infra/linea/config.py](./infra/linea/config.py)
6. [infra/linea/sensor.py](./infra/linea/sensor.py)
7. [infra/linea/archivador.py](./infra/linea/archivador.py)
8. [infra/linea/cli.py](./infra/linea/cli.py)
9. [infra/linea/panel.py](./infra/linea/panel.py)
10. [infra/linea/metricas.py](./infra/linea/metricas.py)

Then move to the module docs in [labs/](./labs/).

## 17. Final summary

This repository is a hands-on industrial AI simulation.

It teaches you how a manufacturing line sends data, stores it, monitors it, visualizes it, and later uses it for AI.

The key idea is:

A reliable industrial system starts with data quality, observability, and proper architecture — not with a model alone.

That is the core lesson of this project.

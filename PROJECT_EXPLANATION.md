# Project explanation: IA Industria 201

This project is a hands-on industrial AI training environment. It simulates a machining station called EST-01 and teaches how industrial data, monitoring, and AI fit together in a real operating context.

The idea is not to build a real factory. Instead, the project creates a realistic simulation of a production line with:

- sensors publishing live values
- an MQTT message broker
- a local SQLite historical database
- dashboards and monitoring tools
- industrial protocols such as OPC UA and Modbus
- AI and LLM services
- lab commands that validate each step

The project is meant to teach the full path of a data-driven industrial solution from machine signals to reports, alerts, and AI models.

## 1. What this project is about

The root README explains the course structure: the project is organized as modules, each focused on one concept.

The general flow is:

1. Data is produced by a process or machine
2. The data is transported through an industrial messaging layer
3. The data is stored in a system of record
4. The data is observed through metrics and dashboards
5. Models are trained or used to make predictions or detect issues
6. Operators or systems react based on the result

This is the industrial AI lifecycle.

## 2. Main learning flow

This repository follows a module-based learning path:

- M01: data architecture, supervision, monitoring, alerts
- M02: data acquisition and integration
- M03: machine learning for prediction and anomaly detection
- M04: computer vision for quality control
- M05: generative AI and local LLMs
- M06: edge AI and industrial integration
- M07: MLOps, observability, and operations
- M08: cybersecurity and governance

You do not start with a model. You start with the data pipeline.

That is a very important idea in this project: the AI layer is only useful when the data path is correct and observable.

## 3. Repository map

The main folders and files are:

- [README.md](./README.md) — main course entry point
- [labs/](./labs/) — module theory and labs
- [infra/](./infra/) — Docker environment, runtime scripts, and project services
- [infra/data/](./infra/data/) — live state and historical database
- [infra/linea/](./infra/linea/) — Python services and logic used by the line
- [infra/prometheus/](./infra/prometheus/) — Prometheus configuration and alerts
- [infra/modelos/](./infra/modelos/) — local model files (not always committed)

## 4. The Docker environment: how the system starts

The most important file for understanding the system is [infra/docker-compose.yml](./infra/docker-compose.yml).

This file defines the services that run together to simulate the industrial line.

### Main services

- `mosquitto` — MQTT broker
- `sensor` — produces machine telemetry and state
- `archivador` — listens to MQTT and writes historical data to SQLite
- `calidad` — simulates quality inspection
- `opcua` — exposes the same data through OPC UA
- `modbus` — exposes the same data through Modbus TCP
- `panel` — Streamlit dashboard for operators
- `llm` — local large language model service
- `api` — FastAPI inference service
- `prometheus` — metrics collection and alerting
- `lab` — lab runner used to validate tasks

These services are all part of one simulated industrial architecture.

## 5. Docker image creation

The base image is defined in [infra/Dockerfile](./infra/Dockerfile).

This file does the following:

- uses `python:3.12-slim-bookworm`
- sets Python environment variables
- installs requirements from [infra/requirements.txt](./infra/requirements.txt)
- installs the `llama-cpp-python` wheel used by the model runtime
- installs additional packages such as `diskcache`
- copies the project code from [infra/linea/](./infra/linea/)

This means every service in the simulation runs from the same Python environment and same app codebase.

The project is built around containerized services, not direct local execution, so the Docker setup is essential to understanding everything else.

## 6. The real project flow: from Docker to reports

The complete flow is best understood as a chain.

### Step 1 — Docker starts the services

When you run:

```bash
docker compose up -d mosquitto sensor archivador
```

you start the message broker and the first data-producing services.

### Step 2 — the sensor generates production data

The main source of the process is [infra/linea/sensor.py](./infra/linea/sensor.py).

This file simulates a machining station and produces a cycle for each piece. Each cycle includes values such as:

- `pieza_id`
- `secuencia`
- `temperatura_c`
- `vibracion_mm_s`
- `corriente_a`
- `tiempo_ciclo_s`
- `ts`

These are the live machine signals.

This sensor also:

- writes the current station state to [infra/data/estado.json](./infra/data/estado.json)
- publishes a JSON message to an MQTT topic
- emits Prometheus metrics
- simulates microstops and thermal behavior

This is the origin of the entire industrial data pipeline.

### Step 3 — MQTT transports the data

The system uses MQTT as the transport layer.

The broker is `mosquitto`. The project uses topics such as:

- `linea/est01/ciclo`
- `linea/est01/evento`
- `linea/est01/consigna`

The important idea is that MQTT is not a database. It is a delivery bus. It distributes events to whoever is subscribed, but it does not permanently store the messages.

This is central to the course: a real industrial data architecture requires both a transport layer and a storage layer.

### Step 4 — the historian stores the data

The service that preserves the data is [infra/linea/archivador.py](./infra/linea/archivador.py).

It subscribes to the cycle messages and stores them in SQLite in [infra/data/historial.sqlite](./infra/data/historial.sqlite).

The database table is typically called `lecturas`, and each row captures one production record.

This is where the project turns transient machine events into historical data.

### Step 5 — the state file keeps the live snapshot

The sensor writes the current machine state to [infra/data/estado.json](./infra/data/estado.json).

This file is a practical snapshot of the current production condition, useful for local checks, dashboards, and integration with other services.

### Step 6 — monitoring and metrics are exposed

The project uses Prometheus and custom metric definitions.

The relevant files are:

- [infra/linea/metricas.py](./infra/linea/metricas.py)
- [infra/prometheus/prometheus.yml](./infra/prometheus/prometheus.yml)
- [infra/prometheus/alertas.yml](./infra/prometheus/alertas.yml)

These files define web endpoints and alert rules so you can monitor the system, detect drift, and identify operational issues that do not always surface as explicit errors.

This is the observability layer: it captures the state of the machine even when there is no failure message.

### Step 7 — dashboards and supervision provide human understanding

The dashboard is built through [infra/linea/panel.py](./infra/linea/panel.py).

It reads from the historical database and presents a simple operational view.

This is the point where plant operators can see:

- live readings
- historical values
- thresholds
- whether the line is behaving normally

The project teaches that a dashboard is useful only if the data is timely, correctly labeled, and trustworthy.

### Step 8 — lab validation uses CLI commands

The backbone of the lab workflow is [infra/linea/cli.py](./infra/linea/cli.py).

This file defines commands like:

- `cmd_m01_01`
- `cmd_m01_02`
- `cmd_m02_01`
- `cmd_modbus`
- `cmd_opcua`
- `sql`
- `resumen`
- `notas`

These commands are used to validate every exercise, and they usually check whether:

- MQTT messages are arriving
- the historical database has records
- the panel responds
- OPC UA or Modbus agree with the live state
- thresholds and metrics are behaving as expected

This is the “proof” layer: a lab passes only if the pipeline is working end-to-end.

### Step 9 — reports and outputs are created

As the project advances, the system creates output files like:

- `historial.sqlite`
- `estado.json`
- CSV datasets
- quality reports
- JSONL logs
- model artifacts

Many of these are stored under [infra/data/](./infra/data/) or in module-specific directories.

The reporting layer is important because industrial AI is not just about a model score. It is about the quality, traceability, and operational interpretation of the data behind the decision.

## 7. How the project teaches industrial thinking

This project is intentionally designed to teach the difference between:

- OT (operational technology): production systems, PLCs, sensors, cycles, safety
- IT (information technology): databases, dashboards, reports, APIs
- AI: models that infer, predict, or assist

The workflow is:

```
plant problem -> data capture -> transport -> storage -> dashboards -> metrics -> model -> action
```

The important thing is that AI does not begin at the model. It begins at the signal.

Without data quality, timestamping, and observability, the model is not trustworthy.

## 8. Core files to study first

If you only want to understand the project in the shortest time, study these files in order:

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
11. [labs/M01-ia-industrial-arquitectura/README.md](./labs/M01-ia-industrial-arquitectura/README.md)

Then continue with later module files when you are ready for the ML and AI stages.

## 9. Why this project matters

The strongest conceptual lesson of this project is that industrial AI must be built on a reliable data architecture.

A production system can fail in several ways:

- no telemetry
- delayed telemetry
- duplicate data
- missing data
- bad timestamps
- wrong units
- poor alerting
- model output with no operational context

This project teaches you to check and fix exactly those problems before building an AI solution.

## 10. Final summary

The project is a simulated factory where:

- a sensor publishes live data
- MQTT distributes the data
- the historian stores it
- Prometheus monitors it
- dashboards visualize it
- CLI commands validate the pipeline
- models are trained and consumed later in the course

The key message is:

Industrial AI is not just a model. It is a complete data and operational architecture that must be trustworthy, observable, and explainable.

This repository teaches that from the very beginning.

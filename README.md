# Snowflake Data Lineage & Observability Platform
A production-ready data observability and lineage framework built to monitor dbt workflows executing on a Snowflake Data Warehouse. This project integrates automated data lineage tracking (OpenLineage) with a unified monitoring stack consisting of Prometheus, Grafana, Loki, Promtail, and Marquez.


## 🏗️ System Architecturetext
```

                  +----------------------------------------+

                  |               Snowflake                |
                  |            (Data Warehouse)            |
                  +----------------------------------------+
                                      ^
                                      | Queries & Execution
                                      v
+------------------+       Executes Models        +--------------------+

|  OpenLineage /   | ---------------------------> |    dbt Project     |
|   Marquez UI     | <--- Sends Lineage Metadata - |  (Transformations) |
+------------------+                              +--------------------+
                                                            |
                                                            | Generates Logs
                                                            v
+------------------+         Pushes Logs          +--------------------+

|   Grafana Loki   | <--------------------------- |      Promtail      |
+------------------+                              |    (Log Agent)     |
        |                                         +--------------------+
        |
        | Query Logs
        v
+------------------+       Scrapes Metrics        +--------------------+

|     Grafana      | <--------------------------- |     Prometheus     |
|   (Dashboards)   |                              |  (Metrics Server)  |
+------------------+                              +--------------------+
                                                            ^
                                                            | Pulls Host Stats
                                                  +--------------------+

                                                  |   Node Exporter    |
                                                  +--------------------+
```


## 🛠️ Technology Stack
### Data Warehouse: 
> Snowflake (Cloud analytical database Engine)
### Data Transformation & Lineage:
> dbt (Database transformation tool)
> Marquez (OpenLineage-compliant metadata repository and lineage visualizer)
### Log Analytics Stack:
> Promtail v3.0.0 (Log shipping agent matching system and docker engine sockets)
> Grafana Loki v3.0.0 (Log aggregation system optimized for log streams)
###  Metrics Stack:
> Node Exporter v1.7.0 (Hardware and hardware host performance metrics exporter)
> Prometheus v2.51.0 (Time-series monitoring database with 30-day data retention)
### Visualization Portal: 
> Grafana v10.4.0 (Preloaded with the grafana-snowflake-datasource plugin)

### 📁 Directory Structure
```
├── .venv/                      # Python virtual environment (dbt dependencies)
├── dbt_project/                # dbt models, snapshots, seeds, and macros
├── logs/                       # System and application execution logs
├── marquez/                    # Marquez storage engine configurations
├── monitoring/                 # Centralized Observability Configuration Suite
│   ├── grafana/                # Grafana configs (plugins & dashboards)
│   ├── loki/                   # loki-config.yml storage policies
│   ├── prometheus/             # prometheus.yml targets and scrape intervals
│   └── promtail/               # promtail-config.yml system log targets
├── .env                        # Local database passwords & configuration values
├── .gitignore                  # Git tracking exclusion list (protects secrets)
├── docker-compose.yml          # Infrastructure orchestration deployment script
└── README.md                   # System documentation
```

## 🔧 Installation & Setup

### Prerequisites
> Docker & Docker Compose installed on the host machine.
> An existing, running external Docker network named marquez_default (created by your Marquez setup):
```
docker network create marquez_default
```

> Python 3.9+ with dbt-snowflake installed within your .venv.

## Initialize Environment
Clone the repository to your host system and navigate into the root directory:
```
git clone <your-repository-url>
cd practice_2
```
## Configure Environment Secrets
> Create a .env file in the project root to securely pass account parameters to your dbt runtime environment:

```
GRAFANA_PORT
GRAFANA_ADMIN_USER
GRAFANA_ADMIN_PASSWORD

PROMETHEUS_PORT

LOKI_PORT

NODE_EXPORTER_PORT

MARQUEZ_API_HOST
MARQUEZ_API_PORT
MARQUEZ_DB_HOST
MARQUEZ_DB_PORT
MARQUEZ_DB_USER
MARQUEZ_DB_PASSWORD
MARQUEZ_DB_NAME

SNOWFLAKE_ACCOUNT
SNOWFLAKE_USER
SNOWFLAKE_PASSWORD
SNOWFLAKE_DATABASE
SNOWFLAKE_WAREHOUSE
SNOWFLAKE_SCHEMA
SNOWFLAKE_ROLE
```

## Deploy the Monitoring Infrastructure
> Spin up the observability services, network bridges, and host volumes in the background using Docker Compose:
```
docker-compose up -d
```
> Verify that all core monitoring components are active:
```
docker compose ps
```

## Run the Data Transformation Pipeline
> To process database objects in Snowflake and automatically broadcast lineage events into Marquez, execute your dbt project:

```
source .venv/bin/activate
cd dbt_project
dbt run
```

## 📊 Infrastructure Access Points
> Once initialization finishes, services can be evaluated using your web browser through the following network endpoints:
```
Service      Host                                                Default Access
Application  Port         External Endpoint URL                   Credentials
Grafana UI   3001         http://localhost:3001            User: admin | Pass: admin123
Prometheus   9090         http://localhost:9090                   None Required
Loki API     3100         http://localhost:3100                   None Required
Node         9100         http://localhost:9100                   None Required
Promtail   Internal       Mapped to /var/log & Docker Socket      None Required
```

## 🔒 Security & Volume Management

### Credential Leakage: 
> Never remove .env from the project's .gitignore file. Plain-text Snowflake administrative keys must never be committed to source code repositories.
### Grafana Plugins: 
> The stack is explicitly configured to load the unsigned grafana-snowflake-datasource plugin located in ./grafana/plugins. Do not delete this directory.
### Data Retention: 
> Prometheus metrics are explicitly pinned to a 30-day retention window via configuration flags (--storage.tsdb.retention.time=30d).
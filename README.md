# ChrysosDemo - Photon Assay Data Processing System

## Project Overview

ChrysosDemo is a demonstration project for processing and analyzing photon assay data from spectroscopic instruments. The system collects data from simulated photon assay devices, processes it through a streaming pipeline, stores it in a database, transforms it for analytics, and visualizes the results.

The project showcases a complete data engineering pipeline using modern technologies:
- **Data Streaming**: Apache Kafka for real-time data ingestion
- **Data Storage**: PostgreSQL for structured data storage
- **Data Transformation**: dbt (data build tool) for analytics transformations
- **Data Visualization**: Grafana for dashboards and monitoring

## System Architecture

```
Producer → Kafka → Consumer → PostgreSQL → dbt → PostgreSQL → Grafana
```

1. **Producers** simulate photon assay devices generating spectral data
2. **Kafka** handles the streaming data pipeline
3. **Consumers** process the data and store it in PostgreSQL
4. **dbt** transforms the raw data into analytics models
5. **Grafana** visualizes the data through dashboards

## Components

### Kafka Services

- **Producers**:
  - `sim_PhotonAssay.py`: Simulates a photon assay device generating spectral data
  - `sim_Temperature.py`: Simulates temperature sensor data

- **Consumers**:
  - `photon_assay_consumer.py`: Processes photon assay data and stores it in PostgreSQL
  - `temperature_consumer.py`: Processes temperature sensor data and stores it in PostgreSQL

### Database

The PostgreSQL database stores:
- Raw sensor data (temperature)
- Photon assay events
- Device information
- Spectrum data with energy levels and intensities

### dbt Models

The dbt project transforms the raw data into analytics models:
- `photon_assay_analytics.sql`: Provides analytics on photon assay data
- `photon_assay_daily_report.sql`: Generates daily reports
- `photon_assay_spectrum_analysis.sql`: Analyzes spectrum data
- `sensor_analytics.sql`: Analyzes temperature sensor data

### Visualization

Grafana dashboards visualize the analytics models from PostgreSQL.

## Setup and Installation

### Prerequisites

- Docker and Docker Compose
- Environment variables:
  - `POSTGRES_PASSWORD`: Password for PostgreSQL
  - `GRAFANA_ADMIN_PASSWORD`: Password for Grafana admin user

### Installation Steps

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ChrysosDemo
   ```

2. Create a `.env` file with the required environment variables:
   ```
   POSTGRES_PASSWORD=your_secure_password
   GRAFANA_ADMIN_PASSWORD=your_grafana_password
   ```

3. Start the services:
   ```
   docker-compose up -d
   ```

4. Initialize the database (first time only):
   ```
   docker-compose exec postgres psql -U chrysosdemo -d chrysosdemo -f /var/lib/postgresql/data/create_tables.sql
   ```

5. Run dbt models:
   ```
   docker-compose exec dbt dbt run
   ```

## Usage

### Monitoring Data Flow

1. Access Kafka topics:
   ```
   docker-compose exec kafka kafka-topics --list --bootstrap-server kafka:9092
   ```

2. View PostgreSQL data:
   ```
   docker-compose exec postgres psql -U chrysosdemo -d chrysosdemo
   ```

3. Access Grafana dashboards:
   Open `http://localhost:3000` in your browser and log in with admin credentials.

### Running dbt Models

```
docker-compose exec dbt dbt run
```

### Stopping the System

```
docker-compose down
```

To remove volumes as well:
```
docker-compose down -v
```

## Project Structure

```
ChrysosDemo/
├── Architecture.puml           # Architecture diagram
├── database/
│   └── create_tables.sql       # Database schema
├── dbt_project/
│   ├── dbt_project.yml         # dbt project configuration
│   ├── profiles.yml            # dbt connection profiles
│   └── models/                 # dbt transformation models
├── docker-compose.yml          # Docker services configuration
└── kafka_services/
    ├── Dockerfile              # Kafka services Dockerfile
    ├── consumer/               # Kafka consumers
    └── producer/               # Kafka producers
```

## Development

To extend the project:
1. Add new producers in `kafka_services/producer/`
2. Add new consumers in `kafka_services/consumer/`
3. Update database schema in `database/create_tables.sql`
4. Create new dbt models in `dbt_project/models/`
5. Configure new Grafana dashboards

## License

[Specify license information]
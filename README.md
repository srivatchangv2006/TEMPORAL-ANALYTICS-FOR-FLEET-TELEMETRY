# TEMPORAL ANALYTICS FOR FLEET TELEMETRY

A real-time analytics project for fleet vehicle telemetry using Kafka for data streaming and Azure Blob Storage for data persistence. The project includes a data producer, a consumer for vehicle data, and a dashboard for analytics.

## Features
- Real-time data ingestion from vehicles
- Kafka-based streaming architecture
- Data storage in Azure Blob
- Temporal analytics and dashboard visualization

## Prerequisites
- Python 3.7+
- Kafka (local or remote)
- Azure Blob Storage account

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Kafka:**
   - Download and install Kafka from [Apache Kafka Downloads](https://kafka.apache.org/downloads).
   - Start Zookeeper and Kafka server:
     ```bash
     # Start Zookeeper
     bin/zookeeper-server-start.sh config/zookeeper.properties
     # Start Kafka
     bin/kafka-server-start.sh config/server.properties
     ```
   - Create the required topic (e.g., `vehicle-data`):
     ```bash
     bin/kafka-topics.sh --create --topic vehicle-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
     ```

4. **Configure Azure Blob Storage:**
   - Set your Azure Blob credentials as environment variables or in a `.env` file (see code for details).

## How to Run

- **Producer:**
  ```bash
  python producer.py
  ```
- **Consumer:**
  ```bash
  python consumer_for_vehicle.py
  ```
- **Dashboard/Analytics:**
  ```bash
  python vehicle.py
  ```

## Running with Docker

You can run the entire stack (Kafka, Zookeeper, and your app) using Docker and Docker Compose.

### Steps:

1. **Install Docker Desktop**
   - Download and install from [Docker Desktop](https://www.docker.com/products/docker-desktop/).

2. **Clone this repository and navigate to the project directory:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

3. **Set your Azure Blob connection string:**
   - Option 1: Edit the `docker-compose.yml` file and set the value for `AZURE_STORAGE_CONNECTION_STRING` under `app:`.
   - Option 2: Create a `.env` file in your project root with:
     ```
     AZURE_STORAGE_CONNECTION_STRING=your_connection_string
     ```

4. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```
   - This will start Zookeeper, Kafka, and your app (by default, runs `python producer.py`).

5. **To run the consumer or dashboard instead:**
   - Edit the `command:` line under `app:` in `docker-compose.yml` to:
     ```yaml
     command: python consumer_for_vehicle.py
     ```
     or
     ```yaml
     command: python vehicle.py
     ```
   - Then re-run:
     ```bash
     docker-compose up --build
     ```

6. **Stopping everything:**
   - Press `Ctrl+C` in the terminal, then run:
     ```bash
     docker-compose down
     ```

7. **(Optional) View logs:**
   - To see logs for your app:
     ```bash
     docker-compose logs app
     ```

> **Note:** Docker and Docker Compose files are provided for convenience. If you do not have Docker, you can run the project locally using the instructions above.

## Screenshots / GIFs

_Add screenshots or GIFs of your dashboard/analytics output here._

## Demo Video

_You can find an informal demo video in [your language] here: [link to video]._

## License

MIT License (or your preferred license)

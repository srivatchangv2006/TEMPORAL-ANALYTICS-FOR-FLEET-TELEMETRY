<img width="1647" height="860" alt="image" src="https://github.com/user-attachments/assets/ba0e7c77-3db5-40d6-8de9-182111e2bf84" /># TEMPORAL ANALYTICS FOR FLEET TELEMETRY

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

## 🗺️ Folium Map Output
COMPLETE TRIP:
Description: The black dots signify the unloaded phase of the trip and the blue ones show when the vehicle is loaded
<img width="1647" height="860" alt="image" src="https://github.com/user-attachments/assets/bd66601c-6b45-46b8-a041-39c4d6841d9f" />
HARSH DRIVING BEHAVIOUR:
Description: The marked points are those where the driver had a harsh driving(overspeeding,sudden brake movement)
<img width="1602" height="796" alt="image" src="https://github.com/user-attachments/assets/34336293-25fd-4196-af34-0fb946123919" />

## ML MODEL PERFORMANCE: 
TRAINING DATA:
<img width="1487" height="993" alt="image" src="https://github.com/user-attachments/assets/238f4e9a-41cd-43e6-96b7-079c23733a02" />
TESTING DATA:
<img width="1486" height="968" alt="image" src="https://github.com/user-attachments/assets/ac85063e-3ac7-4f36-b37a-94459351e88f" />
ML MODEL(LSTM):
<img width="1733" height="761" alt="image" src="https://github.com/user-attachments/assets/ca525e2b-b3a7-418f-88ca-f60186fcedab" />



## 📽️ Demo Videos

LINK: https://ssneduin-my.sharepoint.com/:f:/g/personal/srivatchan23110183_snuchennai_edu_in/EhLcAFOqCVREityYsYrh1WgBroZl8J2mw2ABgJxXqqZnzw?e=l030Y8

These videos walk through different parts of my project. I’ve mainly used English while explaining, but I’ve also included some informal Tamil for better clarity.

The videos cover:

Displaying data on an interactive Folium map

Training and testing the ML model

Showing Prediction vs Actual comparison

Running the Python command-line interface

Explaining the flow from Kafka Producer → Kafka Consumer → Azure Blob Storage → Azure Analytics

(Note: These videos are informal and made to explain the concepts clearly in a mix of English and Tamil.)

from kafka import KafkaProducer #type: ignore
import json
from datetime import datetime #type:ignore
import os
# Replace with your actual Event Hubs Kafka settings
BOOTSTRAP_SERVERS = 'demoproject.servicebus.windows.net:9093'
EVENTHUB_CONNECTION_STRING = os.getenv('EVENTHUB_CONNECTION_STRING')
EVENTHUB_TOPIC = 'my-demo'

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    security_protocol='SASL_SSL',
    sasl_mechanism='PLAIN',
    sasl_plain_username='$ConnectionString',
    sasl_plain_password=EVENTHUB_CONNECTION_STRING,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

# Example message
message = {
    'VehicleID': 'VH010',
    'Latitude': '12.48',
    'Longitude':'77.942',
    'InstanceType':'travel',
    'Timestamp':timestamp,
    'Vehicle Speed[km/h]':'79.3241',
    'Engine RPM[RPM]':'2643',
    'MAF[g/sec]':'13.423',
    'Estimated_Fuel_Rate_L_per_hr':'2.78',
    'Fuel_Added_Liters':"0",
    'Distance_Travelled_km':"10.00",    
    'Loaded':'no'
}
producer.send(EVENTHUB_TOPIC, message)
producer.flush()

print("message sent to azure event hub")

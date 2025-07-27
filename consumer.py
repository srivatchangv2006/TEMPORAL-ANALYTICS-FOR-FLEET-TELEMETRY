






from io import BytesIO
from datetime import datetime
from kafka import KafkaConsumer
from azure.storage.blob import BlobServiceClient  # type: ignore
import json
import csv
import time
import io
import numpy as np
import os
# Azure Storage configuration
BOOTSTRAP_SERVERS = 'demoproject.servicebus.windows.net:9093'
CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = "appendcontainer"
CSV_FILE_PATH = "received_messages.csv"
BLOB_NAME = "long_vehicle_trip_logs.csv"
CONSUMER_GROUP = '$Default'
USERNAME = os.getenv('EVENTHUB_USERNAME')
PASSWORD = os.getenv('EVENTHUB_PASSWORD')
EVENTHUB_TOPIC="my-demo"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

consumer = KafkaConsumer(
    EVENTHUB_TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    security_protocol="SASL_SSL",
    sasl_mechanism="PLAIN",
    sasl_plain_username=USERNAME,
    sasl_plain_password=PASSWORD,
    group_id=CONSUMER_GROUP,
    auto_offset_reset="earliest",  
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
)

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

print("Kafka consumer started. Listening for messages...")

while True:
    msg_pack = consumer.poll(timeout_ms=1000)
    for tp, messages in msg_pack.items():
        for message in messages:
            decoded_msg = message.value
            csv_fields=list(decoded_msg.values())
            csv_line = ",".join(csv_fields) + "\n"
            
            try:
                blob_client.append_block(BytesIO(csv_line.encode('utf-8')))
                print("successfully appended data to blob.")
            except Exception as e:
                print(f"failed to append data: {e}")

            # Append to CSV
    #         with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as csv_file:
    #             csv_writer = csv.writer(csv_file)
    #             csv_writer.writerow(decoded_msg.values())
    #             csv_file.flush()  # Ensure immediate write to disk

    #         print(f"[✔] Received and saved: {decoded_msg}")

    #         # Upload to Azure Blob

    #         try:
    #             with open(CSV_FILE_PATH, "rb") as data:
    #                 blob_client.upload_blob(data, overwrite=True)
    #                 print(f"[↑] Uploaded updated CSV to blob '{BLOB_NAME}'")
    #                 break

    #         except Exception as e:
    #             print(f"[x] Failed to upload to Azure: {e}")

    # time.sleep(0.5)  # prevent high CPU usage
    # stream_downloader = blob_client.download_blob()
    # blob_data = stream_downloader.readall()
    # # Read CSV content from bytes
    # csv_file = io.StringIO(blob_data.decode('utf-8'))
    # csv_reader = csv.reader(csv_file)
    # print("Contents of downloaded CSV:")
    # for row in csv_reader:
    #     print(row)








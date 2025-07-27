from azure.storage.blob import BlobServiceClient #type: ignore
import csv
import io
import pandas as pd
from io import BytesIO
import os
CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = "appendcontainer"  # Your container name
BLOB_NAME = "vehicle_trip.csv"  # Use exact blob name, e.g. kafka_data_2025-06-02T12:34:56.csv

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

# Download blob content
stream_downloader = blob_client.download_blob()
blob_data = stream_downloader.readall()

# Read CSV content from bytes
csv_file = io.StringIO(blob_data.decode('utf-8'))
csv_reader = csv.reader(csv_file)
df=pd.read_csv(BytesIO(blob_data), header=0)
print(df.tail())



import pandas as pd
import numpy as np
print(df.head())
veh_id='VH008'
vehicle_id=df[:149]
print(vehicle_id.info())
import matplotlib.pyplot as plt
plt.figure(figsize=(12,8))
plt.plot(vehicle_id['Engine RPM[RPM]'])
plt.title("engine rpms")
plt.show()
print(max(vehicle_id['Engine RPM[RPM]']))
from folium import Map, Marker #type: ignore
from folium.plugins import TimestampedGeoJson  #type: ignore
import pandas as pd
import json
from datetime import datetime, timedelta

# Simulate timestamps (if you don't have real ones)
vehicle_id = vehicle_id.reset_index(drop=True)
base_time = datetime.now()
vehicle_id['Timestamp'] = [base_time + timedelta(seconds=i*5) for i in range(len(vehicle_id))]
# Create GeoJSON features for each point
features = []
for i, row in vehicle_id.iterrows():
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [row['Longitude'], row['Latitude']],
        },
        'properties': {
            'time': row['Timestamp'].isoformat(),
            'popup': f"Point {i}",
            'icon': 'circle',
            'iconstyle': {
                'fillColor': 'blue',
                'fillOpacity': 0.6,
                'stroke': 'true',
                'radius': 5
            }
        }
    }
    features.append(feature)

# Wrap into FeatureCollection
geojson = {
    'type': 'FeatureCollection',
    'features': features
}

# Create map
m = Map(location=[vehicle_id['Latitude'].iloc[0], vehicle_id['Longitude'].iloc[0]], zoom_start=13)

# Add timestamped geojson
TimestampedGeoJson(
    data=geojson,
    period='PT5S',
    add_last_point=True,
    auto_play=True,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options='YYYY-MM-DD HH:mm:ss',
    time_slider_drag_update=True
).add_to(m)
# Save map
m.save('animated_trip_map.html')
print(np.mean(vehicle_id['Engine RPM[RPM]']),np.std(vehicle_id['Engine RPM[RPM]']))
new=vehicle_id[vehicle_id['Engine RPM[RPM]']<2959]
plt.figure(figsize=(12,8))
plt.plot(new['Engine RPM[RPM]'])
plt.title("engine rpm <2959")
plt.show()
print(max(new['Engine RPM[RPM]']))
new=vehicle_id[vehicle_id['Engine RPM[RPM]']>2959]
plt.figure(figsize=(12,8))
plt.plot(new['Engine RPM[RPM]'])
plt.title("engine rpm >2959")
plt.show()
plt.figure(figsize=(12,8))
plt.scatter(new['Latitude'],new['Longitude'],label="world",color="blue")
plt.title("lat long for engine rpm>2959")
plt.show()
print(np.min(new['Engine RPM[RPM]']))
# print(new['Latitude'],new['Longitude'])
from folium import Map, Marker #type: ignore
from folium.plugins import TimestampedGeoJson  #type: ignore
import pandas as pd
import json
from datetime import datetime, timedelta

# Simulate timestamps (if you don't have real ones)
new = new.reset_index(drop=True)
base_time = datetime.now()
new['Timestamp'] = [base_time + timedelta(seconds=i*5) for i in range(len(new))]

# Create GeoJSON features for each point
features = []
for i, row in new.iterrows():
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [row['Longitude'], row['Latitude']],
        },
        'properties': {
            'time': row['Timestamp'].isoformat(),
            'popup': f"Point {i}",
            'icon': 'circle',
            'iconstyle': {
                'fillColor': 'blue',
                'fillOpacity': 0.6,
                'stroke': 'true',
                'radius': 5
            }
            
        }
    }
    features.append(feature)

# Wrap into FeatureCollection
geojson = {
    'type': 'FeatureCollection',
    'features': features
}
# Create map
m = Map(location=[new['Latitude'].iloc[0], new['Longitude'].iloc[0]], zoom_start=13)
# Add timestamped geojson
TimestampedGeoJson(
    data=geojson,
    period='PT5S',
    add_last_point=True,
    auto_play=True,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options='YYYY-MM-DD HH:mm:ss',
    time_slider_drag_update=True
).add_to(m)

# Save map
m.save('exceeded_rpm_map.html')








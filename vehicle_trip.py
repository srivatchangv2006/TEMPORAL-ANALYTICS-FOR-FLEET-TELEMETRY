













#vehicle_trip.csv
import os
import csv
import io
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from folium import Map
from folium.plugins import TimestampedGeoJson  # type: ignore
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# Azure Blob Storage setup
CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = "appendcontainer"
BLOB_NAME = "vehicle_trip.csv"

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)
blob_data = blob_client.download_blob().readall()

# Load CSV
df = pd.read_csv(BytesIO(blob_data), header=0)

# Convert MM:SS.s format to datetime
BASE_DATETIME = datetime(2025, 1, 1, 0, 0, 0)
def mmss_to_datetime(tstr, base_time=BASE_DATETIME):
    try:
        minutes, seconds = tstr.strip().split(":")
        total_seconds = int(minutes) * 60 + float(seconds)
        return base_time + timedelta(seconds=total_seconds)
    except:
        return None

df['Parsed_Timestamp'] = df['Timestamp'].apply(mmss_to_datetime)

# Filter trip
vehicle_id = df[df['TripId'] == 1].copy()
vehicle_id['Timestamp'] = vehicle_id['Parsed_Timestamp']

# Preprocess numerics
vehicle_id['Estimated_Fuel_Rate_L_per_hr'] = pd.to_numeric(vehicle_id['Estimated_Fuel_Rate_L_per_hr'], errors='coerce').fillna(0)
vehicle_id['Fuel_Added_Liters'] = pd.to_numeric(vehicle_id['Fuel_Added_Liters'], errors='coerce').fillna(0)
vehicle_id['Distance_Travelled_km'] = pd.to_numeric(vehicle_id['Distance_Travelled_km'], errors='coerce').fillna(0)
vehicle_id['Engine RPM[RPM]'] = pd.to_numeric(vehicle_id['Engine RPM[RPM]'], errors='coerce').fillna(0)
vehicle_id['Vehicle Speed[km/h]'] = pd.to_numeric(vehicle_id['Vehicle Speed[km/h]'], errors='coerce').fillna(0)

# Classify loaded/unloaded segments
loaded, unloaded = [], []
loaded_inside, unloaded_inside = [], []
prev = vehicle_id['Loaded'].iloc[0]
for _, row in vehicle_id.iterrows():
    current = row['Loaded']
    if current == "no":
        if prev == "no":
            unloaded_inside.append(row.tolist())
        else:
            if loaded_inside: loaded.append(loaded_inside)
            loaded_inside, unloaded_inside = [], [row.tolist()]
    elif current == "yes":
        if prev == "yes":
            loaded_inside.append(row.tolist())
        else:
            if unloaded_inside: unloaded.append(unloaded_inside)
            unloaded_inside, loaded_inside = [], [row.tolist()]
    prev = current
if loaded_inside: loaded.append(loaded_inside)
if unloaded_inside: unloaded.append(unloaded_inside)

# Segment Efficiency
def calculate_segment_efficiency(segment):
    if len(segment) < 2:
        return None
    try:
        t0 = mmss_to_datetime(segment[0][4])
        t1 = mmss_to_datetime(segment[-1][4])
        time_seconds = (t1 - t0).total_seconds()
        if time_seconds <= 0: return None
        time_hours = time_seconds / 3600.0
        dist_km = float(segment[-1][10]) - float(segment[0][10])
        if dist_km <= 0: return None
        total_fuel = sum(float(r[8]) * (1/60) for r in segment)
        if total_fuel == 0: return None
        return round(dist_km / total_fuel, 2)
    except Exception as e:
        print(f"Error in segment: {e}")
        return None

loaded_efficiencies = [calculate_segment_efficiency(seg) for seg in loaded]
unloaded_efficiencies = [calculate_segment_efficiency(seg) for seg in unloaded]

# Plot RPMs
plt.figure(figsize=(12, 8))
plt.plot(vehicle_id['Engine RPM[RPM]'])
plt.title("Engine RPMs")
plt.show()
print("Max RPM:", vehicle_id['Engine RPM[RPM]'].max())


from folium import Map, Marker #type: ignore
from folium.plugins import TimestampedGeoJson  #type: ignore
import pandas as pd
import json
from datetime import datetime, timedelta

# Simulate timestamps (if you don't have real ones)
vehicle_id = vehicle_id.reset_index(drop=True)
base_time = datetime.now()
vehicle_id['Timestamp'] = [base_time + timedelta(seconds=i*5) for i in range(len(vehicle_id))]
features = []
for i, row in vehicle_id.iterrows():
    is_loaded = str(row['Loaded']).strip().lower() == 'yes'

    color = 'blue' if is_loaded else 'black'

    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [row['Longitude'], row['Latitude']],
        },
        'properties': {
            'time': row['Timestamp'].isoformat(),
            'popup': f"Point {i} - Loaded: {row['Loaded']}",
            'icon': 'circle',
            'iconstyle': {
                'fillColor': color,
                'color': color,         # outline color
                'fillOpacity': 1.0,     # full fill
                'stroke': True,
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


# Trip Dashboard
console = Console()
start_time = vehicle_id['Timestamp'].iloc[0]
end_time = vehicle_id['Timestamp'].iloc[-1]
total_time_sec = (end_time - start_time).total_seconds()
total_time_hr = total_time_sec / 3600.0
start_dist = vehicle_id['Distance_Travelled_km'].iloc[0]
end_dist = vehicle_id['Distance_Travelled_km'].iloc[-1]
total_distance = end_dist - start_dist
total_fuel = (vehicle_id['Estimated_Fuel_Rate_L_per_hr'] * (1/60)).sum()
fuel_added = vehicle_id['Fuel_Added_Liters'].sum()
avg_speed = vehicle_id['Vehicle Speed[km/h]'].mean()
max_speed = vehicle_id['Vehicle Speed[km/h]'].max()
avg_rpm = vehicle_id['Engine RPM[RPM]'].mean()
max_rpm = vehicle_id['Engine RPM[RPM]'].max()
harsh_percent = (vehicle_id['Engine RPM[RPM]'] > 2959).sum() / len(vehicle_id) * 100
loaded_eff_mean = np.mean([x for x in loaded_efficiencies if x])
unloaded_eff_mean = np.mean([x for x in unloaded_efficiencies if x])

summary = Table(title="Trip Summary", box=box.ROUNDED)
summary.add_column("Metric", style="cyan", no_wrap=True)
summary.add_column("Value", style="magenta")
summary.add_row("Vehicle ID", str(vehicle_id.iloc[0]['VehicleID']))
summary.add_row("Trip ID", str(vehicle_id.iloc[0]['TripId']))
summary.add_row("Total Distance", f"{total_distance:.2f} km")
summary.add_row("Trip Duration", f"{total_time_hr:.2f} hrs")
summary.add_row("Avg Speed", f"{avg_speed:.2f} km/h")
summary.add_row("Max Speed", f"{max_speed:.2f} km/h")
summary.add_row("Avg RPM", f"{avg_rpm:.2f}")
summary.add_row("Max RPM", f"{max_rpm:.2f}")
summary.add_row("Harsh Driving", f"{harsh_percent:.2f}%")
summary.add_row("Fuel Used (est.)", f"{total_fuel:.2f} L")
summary.add_row("Fuel Added", f"{fuel_added:.2f} L")
summary.add_row("Efficiency (Loaded)", f"{loaded_eff_mean:.2f} km/l" if loaded_eff_mean else "N/A")
summary.add_row("Efficiency (Unloaded)", f"{unloaded_eff_mean:.2f} km/l" if unloaded_eff_mean else "N/A")

console.print(Panel.fit(summary, title=f"🚛 Fleet Trip Dashboard – {vehicle_id.iloc[0]['VehicleID']}", border_style="green"))















print(np.mean(vehicle_id['Engine RPM[RPM]']),np.std(vehicle_id['Engine RPM[RPM]']))
new=vehicle_id[vehicle_id['Engine RPM[RPM]']<3100]
plt.figure(figsize=(12,8))
plt.plot(new['Engine RPM[RPM]'])
plt.title("engine rpm <2959")
plt.show()

print(max(new['Engine RPM[RPM]']))
new=vehicle_id[vehicle_id['Engine RPM[RPM]']>3100]
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








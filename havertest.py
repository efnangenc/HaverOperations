import requests
import json
from haversine import haversine, Unit
from vehicle_list import vehicles
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
import math 



API_URL = "https://"
THRESHOLD_M = 20000  # 10000 m üstündeki atlamalar yok sayılacak
TOKEN = ""  # JWT token ekle
 
def fetch_points(vehicle_value, start_date, end_date):
    headers = {
        "accept": "application/json",
        "authorization": TOKEN,
        "content-type": "application/json"
    }
 
    payload = {
        "start": start_date,
        "end": end_date,
        "vehicle": {
            "value": vehicle_value,
        },
        # "fleet_id": 4699    #gelir
        "fleet_id": 4017   #alagöz
        # "fleet_id": 4154   #arıtek
    }
 
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    # print(response.status_code)
    response.raise_for_status()
    data = response.json()
    print(data)

    if "positions" not in data:
        raise ValueError("API response does not contain 'positions' key.")
    

    # Alan adlarını API'ye göre ayarla
    return [(float(item[0]), float(item[1])) for item in data["positions"]]
 
 
def calculate_total_m(points):
    total_m = 0.0
    last_point = None
 
    for index, point in enumerate(points):
        
        if last_point:
            dist = haversine(last_point, point, unit=Unit.METERS)
            
            if dist <= THRESHOLD_M:  # mantıksız atlamaları filtrele
                total_m += dist
                last_point = point
        if index == 0:
            last_point = point
 
    return total_m
 
 
def calculate(vehicle_value, start_date, end_date):
    points = fetch_points(vehicle_value, start_date, end_date)
    # print("points:", len(points))
    meters = calculate_total_m(points)
    # print(f"Toplam katedilen mesafe: {meters:.2f} metre")
    # print(f"Toplam katedilen mesafe: {meters/1000:.2f} km")
    return f"{meters/1000: .2f}"




vehicle_value = 36390
date = "22.09.2025"
start_in_date = f"{date} 05:00:00"
end_in_date = f"{date} 21:00:00"
start_out1_date = f"{date} 21:00:00"
end_out1_date = f"{date} 23:59:00"
start_out2_date = f"{date} 00:00:00"
end_out2_date = f"{date} 05:00:00"
distance_in_km = calculate(vehicle_value, start_in_date, end_in_date)
distance_out1_km = calculate(vehicle_value, start_out1_date, end_out1_date)
distance_out2_km = calculate(vehicle_value, start_out2_date, end_out2_date)
distance_out_km = float(distance_out1_km) + float(distance_out2_km)

print(distance_in_km)
print(distance_out_km)
import pandas as pd
import random

# Load data
products_path = "C:\\Users\\Administrator\\Desktop\\Python\\ML\\DataSets\\RawDataSets\\products\\products.csv"
warehouse_path = "C:\\Users\\Administrator\\Desktop\\Python\\ML\\DataSets\\RawDataSets\\warehouse_inventory\\warehouse_inventory.csv"
output_path = "C:\\Users\\Administrator\\Desktop\\Python\\ML\\DataSets\\RawDataSets\\transports\\transports.csv"

df_products = pd.read_csv(products_path)
df_warehouse = pd.read_csv(warehouse_path)

# Constants
vehicle_numbers = [f"GJ{random.randint(1, 30):02d}X{random.randint(1000, 9999)}" for _ in range(200)]
route_types = ["InterState", "Intercity"]
status_options = ["Scheduled", "In Transit", "Delivered", "Delayed"]
locations = ["Ahmedabad", "Surat", "Baroda", "Rajkot", "Mumbai", "Jaipur"]

# Init
used_ids = set()
transports_data = []

for i, row in df_warehouse.iterrows():
    product_id = row["Product_ID"]
    if pd.isna(product_id):
        continue

    product = df_products[df_products["Product_ID"] == product_id]
    if product.empty:
        continue
    prod = product.iloc[0]

    temp_sensitive = prod["Temp_Sensitive_Flag"]
    fragile = prod["Fragile_Flag"]
    uid = product_id.split("-")[-1]

    # Zone/Rack fallback
    zone = row["Zone"] if pd.notna(row["Zone"]) else f"Z{random.randint(1, 3)}"
    rack = row["Rack_Location"] if pd.notna(row["Rack_Location"]) else f"R{random.randint(1, 10)}"

    vehicle_type = "Specialised" if temp_sensitive or fragile else "General"
    vehicle_number = vehicle_numbers[i % len(vehicle_numbers)]

    transport_id = f"{zone}::{rack}::{uid}::{vehicle_number}::{vehicle_type}"
    if transport_id in used_ids:
        continue
    used_ids.add(transport_id)

    route = random.choice(route_types)
    transit_days = random.randint(2, 7) if route == "Intercity" else random.randint(5, 15)

    transports_data.append({
        "Transport_ID": transport_id,
        "Dispatched_Quantity": 0,
        "Vehicle_Type": vehicle_type,
        "Route_Type": route,
        "Start_Location": random.choice(locations),
        "End_Location": random.choice(locations),
        "Estimated_Transit_Days": transit_days,
        "Status": "Scheduled"
    })

# Save
df_transports = pd.DataFrame(transports_data)
df_transports.to_csv(output_path, index=False)
print(f"✅ {len(df_transports)} valid transport records saved → {output_path}")

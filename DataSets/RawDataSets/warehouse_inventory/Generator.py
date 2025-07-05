import pandas as pd
import random
from pathlib import Path

# Load
products_df = pd.read_csv(r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\products\products.csv")

# Zone logic
def determine_zone(temp, fragile):
    if temp and fragile:
        return "ZONE-1"
    elif temp:
        return "ZONE-2"
    elif fragile:
        return "ZONE-3"
    else:
        return "ZONE-4"

products_df["Zone"] = products_df.apply(lambda x: determine_zone(x["Temp_Sensitive_Flag"], x["Fragile_Flag"]), axis=1)

# Rack Setup (10 racks per zone, 5 pallet per rack)
racks_per_zone = {zone: [f"RACK-{i+1}" for i in range(10)] for zone in products_df["Zone"].unique()}
rack_capacity = 250  # Adjust this based on volume or weight in real setup

# Init
inventory_data = []
used_storage_ids = set()
rack_indices = {z: 0 for z in racks_per_zone}
pallet_count = {z: 0 for z in racks_per_zone}

# Inventory Allocation
for _, prod in products_df.iterrows():
    quantity = prod["Quantity_Available"]
    zone = prod["Zone"]
    racks = racks_per_zone[zone]
    product_id = prod["Product_ID"]
    uid = product_id.split("-")[-1]

    while quantity > 0:
        rack = racks[rack_indices[zone]]
        store_qty = min(quantity, rack_capacity)

        storage_id = f"{zone}:{rack}:{uid}"
        while storage_id in used_storage_ids:
            uid = str(int(uid) + 1)
            storage_id = f"{zone}:{rack}:{uid}"

        used_storage_ids.add(storage_id)

        inventory_data.append({
            "Storage_ID": storage_id,
            "Product_ID": product_id,
            "Rack_Location": rack,
            "Zone": zone,
            "Stored_Quantity": store_qty,
            "FIFO_Flag": int(prod["Expiry_Date"] != "")  # assume non-empty expiry = FIFO
        })

        quantity -= store_qty
        pallet_count[zone] += 1

        # Move to next rack if pallet count full
        if pallet_count[zone] >= 5:
            rack_indices[zone] = (rack_indices[zone] + 1) % len(racks)
            pallet_count[zone] = 0

# Save
warehouse_path = Path("C:/Users/Administrator/Desktop/Python/ML/DataSets/RawDataSets/warehouse_inventory/warehouse_inventory.csv")
pd.DataFrame(inventory_data).to_csv(warehouse_path, index=False)
print(f"✅ Warehouse inventory saved: {warehouse_path}")

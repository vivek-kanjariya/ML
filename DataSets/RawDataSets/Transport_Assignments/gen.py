import pandas as pd
import random
from datetime import datetime, timedelta

# File paths
products_path = r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\products\products.csv"
warehouse_path = r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\warehouse_inventory\warehouse_inventory.csv"
transports_path = r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\transports\transports.csv"
output_path = r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\transport_assignments\transport_assignments.csv"

# Load files
df_products = pd.read_csv(products_path)
df_warehouse = pd.read_csv(warehouse_path)
df_transports = pd.read_csv(transports_path)

assignments = []
used_ids = set()

for _, product in df_products.iterrows():
    product_id = product["Product_ID"]
    uid = product_id.split("-")[-1]
    fragile = product["Fragile_Flag"]
    temp_sensitive = product["Temp_Sensitive_Flag"]
    
    # Search for warehouse row
    wh_rows = df_warehouse[df_warehouse["Product_ID"] == product_id]
    if not wh_rows.empty:
        wh_row = wh_rows.sample(1).iloc[0]  # Random warehouse if multiple
        zone = wh_row["Zone"]
        rack = wh_row["Rack_Location"]
    else:
        zone = f"Z{random.randint(1, 3)}"
        rack = f"R{random.randint(1, 10)}"

    # Search transport row
    tr_rows = df_transports[df_transports["Transport_ID"].str.contains(uid)]
    if not tr_rows.empty:
        tr_row = tr_rows.sample(1).iloc[0]
        transport_id = tr_row["Transport_ID"]
        vehicle_no = transport_id.split("::")[3]
    else:
        vehicle_no = f"GJ{random.randint(10,99)}X{random.randint(1000,9999)}"
        vehicle_type = "Specialised" if fragile or temp_sensitive else "General"
        transport_id = f"{zone}::{rack}::{uid}::{vehicle_no}::{vehicle_type}"

    assignment_id = f"{zone}::{rack}::{uid}::{vehicle_no}"
    if assignment_id in used_ids:
        continue
    used_ids.add(assignment_id)

    # Smart urgency flag: based on Expiry window or fragility
    expiry_days = (pd.to_datetime(product["Expiry_Date"]) - datetime.today()).days
    urgent_flag = 1 if expiry_days < 30 or fragile or temp_sensitive else 0

    # Generate dates
    dispatch_window = datetime.today() + timedelta(days=random.randint(0, 2))
    delivery_window = dispatch_window + timedelta(days=random.randint(2, 4))

    assignments.append({
        "Assignment_ID": assignment_id,
        "Product_ID": product_id,
        "Transport_ID": transport_id,
        "Dispatch_Window": dispatch_window.strftime("%Y-%m-%d"),
        "Delivery_Window": delivery_window.strftime("%Y-%m-%d"),
        "Urgent_Flag": urgent_flag
    })

# Save
df_assignments = pd.DataFrame(assignments)
df_assignments.to_csv(output_path, index=False)
print(f"✅ {len(df_assignments)} Transport Assignments saved → {output_path}")

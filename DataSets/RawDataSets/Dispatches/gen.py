import pandas as pd
import random
from datetime import datetime, timedelta

# ---------------- File paths ----------------
products_path = r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\products\products.csv"
warehouse_path = r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\warehouse_inventory\warehouse_inventory.csv"
transports_path = r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\transports\transports.csv"
assignments_path = r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\transport_assignments\transport_assignments.csv"
output_dispatches = r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\dispatches\dispatches.csv"

# ---------------- Load data ----------------
df_products = pd.read_csv(products_path)
df_warehouse = pd.read_csv(warehouse_path)
df_transports = pd.read_csv(transports_path)
df_assignments = pd.read_csv(assignments_path)

# ---------------- Constants ----------------
operator_ids = [f"OP{random.randint(100, 999)}" for _ in range(300)]
delivery_statuses = ['Delivered', 'In Transit', 'Delayed', 'Failed']
delay_reasons_pool = ["Traffic", "Weather", "Logistics", "Depot Overflow", "Operator Error"]
dispatches = []
used_ids = set()

# ---------------- Helpers ----------------
def extract_vehicle_id(transport_id):
    parts = transport_id.split("::")
    return parts[3] if len(parts) >= 4 else "UNKNOWN"

# ---------------- Main Generation Loop ----------------
for i, row in df_assignments.iterrows():
    assignment_id = row["Assignment_ID"]
    product_id = row["Product_ID"]
    transport_id = row["Transport_ID"]
    uid = product_id.split("-")[-1]
    rack_id = assignment_id.split("::")[1]

    # Available quantity from inventory
    stored_qty = df_warehouse[df_warehouse["Product_ID"] == product_id]["Stored_Quantity"].sum()
    if stored_qty <= 0:
        continue

    qty_dispatched = random.randint(1, min(50, stored_qty))

    # Dispatch timing
    try:
        dispatch_window = pd.to_datetime(row["Dispatch_Window"])
        delivery_window = pd.to_datetime(row["Delivery_Window"])
    except:
        dispatch_window = datetime.today() - timedelta(days=5)
        delivery_window = datetime.today() + timedelta(days=5)

    if dispatch_window >= delivery_window:
        dispatch_date = dispatch_window
    else:
        delta_days = (delivery_window - dispatch_window).days
        dispatch_date = dispatch_window + timedelta(days=random.randint(0, max(1, delta_days)))

    # Delivery status and damage logic
    status = random.choice(delivery_statuses)
    is_damaged = 0
    delay_reason = ""

    if status in ["Delayed", "Failed"]:
        if random.random() < 0.3:
            is_damaged = 1
            delay_reason = random.choice(delay_reasons_pool)
    elif status == "Delivered" and random.random() < 0.05:
        is_damaged = 1
        delay_reason = "Minor Handling Damage"

    # Guarantee non-empty delay_reason if damaged
    if is_damaged == 1 and not delay_reason.strip():
        delay_reason = "Unknown"

    # Unique Dispatch ID
    dispatch_id = f"{uid}::{rack_id}::{str(i).zfill(4)}"
    if dispatch_id in used_ids:
        continue
    used_ids.add(dispatch_id)

    # Append record
    dispatches.append({
        "Dispatch_ID": dispatch_id,
        "Assignment_ID": assignment_id,
        "Quantity_Dispatched": qty_dispatched,
        "Dispatch_Date": dispatch_date.strftime("%Y-%m-%d %H:%M:%S"),
        "Vehicle_ID": extract_vehicle_id(transport_id),
        "Operator_ID": random.choice(operator_ids),
        "Delivery_Status": status,
        "Is_Damaged": is_damaged,
        "Delay_Reason": delay_reason
    })

# ---------------- Save to CSV ----------------
df_dispatches = pd.DataFrame(dispatches)
df_dispatches.to_csv(output_dispatches, index=False)
print(f"✅ Saved {len(dispatches)} dispatches to:\n{output_dispatches}")

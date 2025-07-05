import pandas as pd
import os
from datetime import datetime

# === CONFIG ===
paths = {
    "products": r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\products\products.csv",
    "warehouse": r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\warehouse_inventory\warehouse_inventory.csv",
    "transports": r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\transports\transports.csv",
    "assignments": r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\transport_assignments\transport_assignments.csv",
    "dispatches": r"C:\Users\Administrator\Desktop\Python\ML\DataSets\RawDataSets\dispatches\dispatches.csv",
    "inventory_events": r"C:\Users\Administrator\Desktop\Python\ML\DataSets\events\eventsinventory_events.csv",
    "assignment_logs": r"C:\Users\Administrator\Desktop\Python\ML\DataSets\events\eventsassignment_logs.csv",
    "dispatch_status_logs": r"C:\Users\Administrator\Desktop\Python\ML\DataSets\events\eventsdispatch_status_logs.csv",
    "transport_events": r"C:\Users\Administrator\Desktop\Python\ML\DataSets\events\eventstransport_events.csv"
}

# === HELPERS ===
def validate_date_order(earlier, later):
    try:
        return pd.to_datetime(earlier) < pd.to_datetime(later)
    except:
        return False

def validate_enum(value, allowed_values):
    return str(value).strip() in allowed_values

def is_boolean(val):
    return val in [0, 1, True, False]

def non_empty(val):
    return pd.notna(val) and str(val).strip() != ""

# === LOAD DATA ===
dataframes = {}
logs = []

for key, path in paths.items():
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            dataframes[key] = df
        except Exception as e:
            logs.append(f"[ERROR] Failed to read '{key}': {str(e)}")
    else:
        logs.append(f"[ERROR] File not found: {path}")

# === VALIDATIONS ===

# --- PRODUCTS ---
if "products" in dataframes:
    df = dataframes["products"]
    for i, row in df.iterrows():
        pid = row.get("Product_ID", "")

        if not non_empty(pid):
            logs.append(f"[Products] Row {i}: Missing Product_ID")

        if not validate_date_order(row.get("Manufacture_Date", ""), row.get("Expiry_Date", "")):
            logs.append(f"[Products] {pid}: Manufacture_Date >= Expiry_Date")

        if row.get("Quantity_Available", -1) < 0:
            logs.append(f"[Products] {pid}: Quantity_Available < 0")

        if row.get("Unit_Weight (kg)", 0) <= 0 or row.get("Unit_Weight (kg)", 0) > 3:
            logs.append(f"[Products] {pid}: Invalid Unit_Weight (kg)")

        if row.get("Unit_Volume (L)", 0) <= 0 or row.get("Unit_Volume (L)", 0) > 2:
            logs.append(f"[Products] {pid}: Invalid Unit_Volume (L)")

        if not is_boolean(row.get("Fragile_Flag")):
            logs.append(f"[Products] {pid}: Fragile_Flag not boolean")

        if not is_boolean(row.get("Temp_Sensitive_Flag")):
            logs.append(f"[Products] {pid}: Temp_Sensitive_Flag not boolean")

# --- WAREHOUSE ---
if "warehouse" in dataframes and "products" in dataframes:
    df = dataframes["warehouse"]
    valid_products = set(dataframes["products"]["Product_ID"])

    for i, row in df.iterrows():
        pid = row.get("Product_ID")
        if pid not in valid_products:
            logs.append(f"[Warehouse] Row {i}: Product_ID {pid} not in Products")

        if row.get("Stored_Quantity", -1) < 0:
            logs.append(f"[Warehouse] {pid}: Stored_Quantity < 0")

        if not non_empty(row.get("Zone")) or not non_empty(row.get("Rack_Location")):
            logs.append(f"[Warehouse] {pid}: Zone or Rack_Location missing")

# --- TRANSPORTS ---
if "transports" in dataframes:
    df = dataframes["transports"]
    for i, row in df.iterrows():
        if not validate_enum(row.get("Vehicle_Type", ""), ['Bike', 'Mini-Truck', 'Van', 'Truck', 'General', 'Specialised']):
            logs.append(f"[Transports] Row {i}: Invalid Vehicle_Type")

        if not validate_enum(row.get("Route_Type", ""), ['Direct', 'Hub-Spoke', 'Multimodal', 'Intercity', 'InterState']):
            logs.append(f"[Transports] Row {i}: Invalid Route_Type")

        if not validate_enum(row.get("Status", ""), ['Scheduled', 'In Transit', 'Delivered', 'Delayed', 0]):
            logs.append(f"[Transports] Row {i}: Invalid Status")

# --- ASSIGNMENTS ---
if "assignments" in dataframes:
    df = dataframes["assignments"]
    for i, row in df.iterrows():
        if not validate_date_order(row.get("Dispatch_Window", ""), row.get("Delivery_Window", "")):
            logs.append(f"[Assignments] Row {i}: Dispatch_Window >= Delivery_Window")

        if not is_boolean(row.get("Urgent_Flag", -1)):
            logs.append(f"[Assignments] Row {i}: Urgent_Flag not boolean")

# --- DISPATCHES ---
if "dispatches" in dataframes:
    df = dataframes["dispatches"]
    for i, row in df.iterrows():
        status = row.get("Delivery_Status")
        if not validate_enum(status, ['Delivered', 'In Transit', 'Delayed', 'Failed']):
            logs.append(f"[Dispatches] Row {i}: Invalid Delivery_Status")

        if row.get("Is_Damaged") == 1 and not non_empty(row.get("Delay_Reason")):
            logs.append(f"[Dispatches] Row {i}: Is_Damaged = 1 but Delay_Reason is empty")

        if status == "Delayed" and not non_empty(row.get("Delay_Reason")):
            logs.append(f"[Dispatches] Row {i}: Delayed but Delay_Reason empty")

# --- EVENTS (Optional basic check) ---
event_keys = ["inventory_events", "assignment_logs", "dispatch_status_logs", "transport_events"]
for key in event_keys:
    if key in dataframes:
        df = dataframes[key]
        for i, row in df.iterrows():
            if not non_empty(row.get("Event_ID")):
                logs.append(f"[{key}] Row {i}: Missing Event_ID")
            if not non_empty(row.get("Event_Type")):
                logs.append(f"[{key}] Row {i}: Missing Event_Type")

# === FINAL OUTPUT ===
print("=" * 60)
if not logs:
    print("✅ No validation errors found. All datasets are clean.")
else:
    print(f"❌ {len(logs)} issues found. Showing first 20:")
    for log in logs[:20]:
        print("-", log)

    # Save full logs to file
    with open("validation_logs.txt", "w") as f:
        for log in logs:
            f.write(log + "\n")
    print("📄 Full logs saved to 'validation_logs.txt'")
print("=" * 60)

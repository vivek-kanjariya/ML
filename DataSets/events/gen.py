import pandas as pd
from datetime import datetime, timedelta
import random

# Define correct file paths
base_path = "C:/Users/Administrator/Desktop/Python/ML/DataSets/events"

products_path = "C:/Users/Administrator/Desktop/Python/ML/DataSets/RawDataSets/products/products.csv"
warehouse_path = "C:/Users/Administrator/Desktop/Python/ML/DataSets/RawDataSets/warehouse_inventory/warehouse_inventory.csv"
transports_path = "C:/Users/Administrator/Desktop/Python/ML/DataSets/RawDataSets/transports/transports.csv"
assignments_path = "C:/Users/Administrator/Desktop/Python/ML/DataSets/RawDataSets/Transport_Assignments/Transport_Assignments.csv"
dispatches_path = "C:/Users/Administrator/Desktop/Python/ML/DataSets/RawDataSets/Dispatches/Dispatches.csv"

# Load all sheets
df_products = pd.read_csv(products_path)
df_warehouse = pd.read_csv(warehouse_path)
df_transports = pd.read_csv(transports_path)
df_assignments = pd.read_csv(assignments_path)
df_dispatches = pd.read_csv(dispatches_path)

# Create EventLogs folder if not exist
import os
os.makedirs(base_path, exist_ok=True)

# --- 1. Inventory Events ---
inventory_events = df_warehouse.copy()
inventory_events["Event_Type"] = "Stored"
inventory_events["Event_Date"] = pd.to_datetime("today").normalize()
inventory_events["Event_ID"] = ["INV-" + str(i).zfill(5) for i in range(len(inventory_events))]

inventory_events = inventory_events[[
    "Event_ID", "Product_ID", "Zone", "Rack_Location", "Stored_Quantity", "FIFO_Flag", "Event_Type", "Event_Date"
]]
inventory_events.to_csv(base_path + "inventory_events.csv", index=False)

# --- 2. Dispatch Events ---
dispatch_logs = df_dispatches.copy()
dispatch_logs["Event_ID"] = ["DSP-" + str(i).zfill(5) for i in range(len(dispatch_logs))]
dispatch_logs["Event_Date"] = pd.to_datetime(dispatch_logs["Dispatch_Date"])
dispatch_logs["Event_Type"] = dispatch_logs["Delivery_Status"]

dispatch_logs = dispatch_logs[[
    "Event_ID", "Assignment_ID", "Dispatch_Date", "Vehicle_ID", "Delivery_Status", "Is_Damaged", "Delay_Reason", "Event_Type", "Event_Date"
]]
dispatch_logs.to_csv(base_path + "dispatch_status_logs.csv", index=False)

# --- 3. Transport Events ---
transport_events = df_transports.copy()
transport_events["Event_ID"] = ["TRN-" + str(i).zfill(5) for i in range(len(transport_events))]
transport_events["Event_Type"] = "Transport Scheduled"
transport_events["Event_Date"] = pd.to_datetime("today").normalize()

transport_events = transport_events[[
    "Event_ID", "Transport_ID", "Vehicle_Type", "Route_Type", "Status", "Estimated_Transit_Days", "Event_Type", "Event_Date"
]]
transport_events.to_csv(base_path + "transport_events.csv", index=False)

# --- 4. Assignment Logs ---
assignment_logs = df_assignments.copy()
assignment_logs["Event_ID"] = ["ASN-" + str(i).zfill(5) for i in range(len(assignment_logs))]
assignment_logs["Event_Date"] = pd.to_datetime("today") - pd.to_timedelta(
    [random.randint(2, 10) for _ in range(len(assignment_logs))], unit="D")
assignment_logs["Event_Type"] = "Assigned"

assignment_logs = assignment_logs[[
    "Event_ID", "Assignment_ID", "Product_ID", "Transport_ID", "Dispatch_Window", "Delivery_Window", "Urgent_Flag", "Event_Type", "Event_Date"
]]
assignment_logs.to_csv(base_path + "assignment_logs.csv", index=False)

print("✅ All 4 event-based sheets created in:", base_path)

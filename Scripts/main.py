import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

# Number of rows to generate
num_entries = 2000

# OrderID format like XXX-XXX-XXX-XXX
def generate_order_id():
    return '-'.join(str(uuid.uuid4()).upper().split('-')[:4])

# Route types and transport mapping
route_types = {
    "Interstate": "Big Truck",
    "Intercity": "Medium Truck",
    "Local": "Small Truck"
}
route_keys = list(route_types.keys())

# Standard pallet sizes (industrial)
standard_pallet_sizes = [60, 80, 100, 120, 150]

yes_no = ["Yes", "No"]

data = []

for _ in range(num_entries):
    order_id = generate_order_id()

    order_date = datetime.today() - timedelta(days=random.randint(1, 7))  # recent orders
    expiry_days = random.randint(60, 730)  # 2 months to 24 months
    expiry_date = order_date + timedelta(days=expiry_days)

    pallet_size = random.choice(standard_pallet_sizes)
    route_type = random.choice(route_keys)
    transport_mode = route_types[route_type]

    urgent = random.choice(yes_no)
    fragile = random.choice(yes_no)
    temp_sensitive = random.choice(yes_no)

    dispatch_window = datetime.today() + timedelta(days=random.randint(1, 7))

    data.append({
        "OrderID": order_id,
        "Order_Date": order_date.strftime('%d/%m/%Y'),
        "Expiry_Date": expiry_date.strftime('%d/%m/%Y'),
        "Pallet_Size": pallet_size,
        "Route_Type": route_type,
        "Mode_of_Transport": transport_mode,
        "Urgent_Order_Flag": urgent,
        "Fragility": fragile,
        "Dispatch_Window": dispatch_window.strftime('%d/%m/%Y'),
        "Temp_Sensitive": temp_sensitive
    })

# Save file
df = pd.DataFrame(data)
file_name = "C:/Users/Administrator/Desktop/Python/DIsssSdata.csv"
df.to_csv(file_name, index=False)

print(f"✅ Dataset saved as: {file_name}")

# Re-import required modules due to code execution environment reset
import pandas as pd
import random
import re
from datetime import datetime, timedelta

def generate_modified_product_dataset_csv(num_rows, output_path):
    products_meta = [
        {"Product_Name": "VeeCal-D Pet", "Category": "Supplements", "Prefix": "SUP", "UID": 434, "Weight": 2.5, "Volume": 1.2},
        {"Product_Name": "VeeWormex Plus", "Category": "Deworming", "Prefix": "DEW", "UID": 795, "Weight": 0.6, "Volume": 0.25},
        {"Product_Name": "VeeVit-L Oral", "Category": "Vitamins & Tonics", "Prefix": "VIT", "UID": 285, "Weight": 0.5, "Volume": 0.3},
        {"Product_Name": "VeeCef Injection 1gm", "Category": "Antibiotics", "Prefix": "ANT", "UID": 789, "Weight": 3.0, "Volume": 1.5},
        {"Product_Name": "VeeOxy-4000", "Category": "Antibiotics", "Prefix": "ANT", "UID": 295, "Weight": 2.8, "Volume": 1.4},
        {"Product_Name": "VeeMune-L", "Category": "Immunity Boosters", "Prefix": "IMM", "UID": 384, "Weight": 1.0, "Volume": 0.6},
        {"Product_Name": "VeeLac Bolus", "Category": "Digestive Aids", "Prefix": "DIG", "UID": 185, "Weight": 1.2, "Volume": 0.7},
        {"Product_Name": "VeeTherm Gel", "Category": "Topical Applications", "Prefix": "TOP", "UID": 854, "Weight": 1.8, "Volume": 1.0}
    ]

    expiry_map = {
        "Supplements": 18,
        "Deworming": 24,
        "Vitamins & Tonics": 12,
        "Antibiotics": 14,
        "Immunity Boosters": 10,
        "Digestive Aids": 16,
        "Topical Applications": 20
    }

    fragile_categories = {"Antibiotics", "Topical Applications"}
    temp_sensitive_categories = {"Antibiotics", "Immunity Boosters"}

    today = datetime.today()
    data = []

    for i in range(num_rows):
        prod = random.choice(products_meta)
        sku_num = 1000 + i
        sku_code = f"SKU-{sku_num}"
        batch_number = f"B{random.randint(10, 99)}"
        product_id = f"{prod['Prefix']}-{sku_num}-{batch_number}-{prod['UID']}"
        manufacture_date = today - timedelta(days=random.randint(0, 3 * 365))
        expiry_months = expiry_map[prod["Category"]]
        expiry_date = manufacture_date + timedelta(days=expiry_months * 30)

        fragile = 1 if prod["Category"] in fragile_categories else 0
        temp_sensitive = 1 if prod["Category"] in temp_sensitive_categories else 0

        data.append({
            "Product_ID": product_id,
            "Product_Name": prod["Product_Name"],
            "SKU_Code": sku_code,
            "Batch_Number": batch_number,
            "Manufacture_Date": manufacture_date.strftime("%Y-%m-%d"),
            "Expiry_Date": expiry_date.strftime("%Y-%m-%d"),
            "Quantity_Available": random.randint(50, 200),
            "Unit_Weight (kg)": prod["Weight"],
            "Unit_Volume (L)": prod["Volume"],
            "Fragile_Flag": fragile,
            "Temp_Sensitive_Flag": temp_sensitive
        })

    df = pd.DataFrame(data)
    df.to_csv("./products.csv", index=False)
    return "./products.csv"

# Generate the modified dataset
generate_modified_product_dataset_csv(6000, "./products.csv")

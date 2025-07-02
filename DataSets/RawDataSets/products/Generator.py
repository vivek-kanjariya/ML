import pandas as pd
import random
import re
from datetime import datetime, timedelta

def generate_complete_product_dataset_csv(num_rows, output_path):
    products_meta = [
        {"Product_Name": "VeeCal-D Pet", "Category": "Supplements", "Prefix": "SUP", "Weight": 2.5, "Volume": 1.2},
        {"Product_Name": "VeeWormex Plus", "Category": "Deworming", "Prefix": "DEW", "Weight": 0.6, "Volume": 0.25},
        {"Product_Name": "VeeVit-L Oral", "Category": "Vitamins & Tonics", "Prefix": "VIT", "Weight": 0.5, "Volume": 0.3},
        {"Product_Name": "VeeCef Injection 1gm", "Category": "Antibiotics", "Prefix": "ANT", "Weight": 3.0, "Volume": 1.5},
        {"Product_Name": "VeeOxy-4000", "Category": "Antibiotics", "Prefix": "ANT", "Weight": 2.8, "Volume": 1.4},
        {"Product_Name": "VeeMune-L", "Category": "Immunity Boosters", "Prefix": "IMM", "Weight": 1.0, "Volume": 0.6},
        {"Product_Name": "VeeLac Bolus", "Category": "Digestive Aids", "Prefix": "DIG", "Weight": 1.2, "Volume": 0.7},
        {"Product_Name": "VeeTherm Gel", "Category": "Topical Applications", "Prefix": "TOP", "Weight": 1.8, "Volume": 1.0}
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
        unique_code = f"Z{random.randint(100, 999)}"
        product_id = f"{prod['Prefix']}-{sku_num}-{batch_number}-{unique_code}"
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
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {num_rows} rows → Saved to: {output_path}")

def validate_product_dataset(filepath):
    df = pd.read_csv(filepath)
    errors = []

    expected_columns = [
        "Product_ID", "Product_Name", "SKU_Code", "Batch_Number",
        "Manufacture_Date", "Expiry_Date", "Quantity_Available",
        "Unit_Weight (kg)", "Unit_Volume (L)", "Fragile_Flag", "Temp_Sensitive_Flag"
    ]
    
    for col in expected_columns:
        if col not in df.columns:
            errors.append(f"Missing expected column: {col}")

    df["Manufacture_Date"] = pd.to_datetime(df["Manufacture_Date"], errors='coerce')
    df["Expiry_Date"] = pd.to_datetime(df["Expiry_Date"], errors='coerce')

    if not (df["Expiry_Date"] > df["Manufacture_Date"]).all():
        errors.append("Some Expiry_Date values are not after Manufacture_Date")

    today = pd.Timestamp(datetime.today())
    if ((today - df["Manufacture_Date"]).dt.days > 3 * 365).any():
        errors.append("Some Manufacture_Date values are older than 3 years")

    if not df["Fragile_Flag"].isin([0, 1]).all():
        errors.append("Fragile_Flag must be 0 or 1")
    if not df["Temp_Sensitive_Flag"].isin([0, 1]).all():
        errors.append("Temp_Sensitive_Flag must be 0 or 1")

    if not df["Product_ID"].is_unique:
        errors.append("Product_IDs are not unique")

    pattern = r'^[A-Z]{3}-\d{4}-B\d{2}-Z\d{3}$'
    if not df["Product_ID"].apply(lambda x: bool(re.match(pattern, str(x)))).all():
        errors.append("Some Product_IDs are not in expected format")

    nulls = df.isnull().sum()
    if (nulls > 0).any():
        errors.append("Null values found in: " + ", ".join(nulls[nulls > 0].index.tolist()))

    if not errors:
        print("✅ VALIDATION PASSED")
    else:
        print("❌ VALIDATION FAILED:")
        for err in errors:
            print("-", err)

# Run both
csv_path = "./products.csv"
generate_complete_product_dataset_csv(6000, csv_path)
validate_product_dataset(csv_path)

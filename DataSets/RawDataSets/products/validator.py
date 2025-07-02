import pandas as pd
import random
import re
from datetime import datetime, timedelta


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


csv_path = "DataSets\RawDataSets\products\Products.csv"
validate_product_dataset(csv_path)
            
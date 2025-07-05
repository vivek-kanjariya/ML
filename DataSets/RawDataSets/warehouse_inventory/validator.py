# Adjust validation logic for only products.csv and warehouse_inventory.csv
import pandas as pd
import re
from datetime import datetime
# Reload the files
inventory_path = "C:\\Users\\Administrator\\Desktop\\Python\\ML\\DataSets\\RawDataSets\\warehouse_inventory\\warehouse_inventory.csv"
products_path = "C:\\Users\\Administrator\\Desktop\\Python\\ML\\DataSets\\RawDataSets\\products\\products.csv"

df_products = pd.read_csv(products_path)
df_inventory = pd.read_csv(inventory_path)

# Validator function using only products and inventory data
def validate_inventory_against_products(products_df, inventory_df):
    errors = []

    # Expected columns
    expected_columns = [
        "Storage_ID", "Product_ID", "Rack_Location", 
        "Zone", "Stored_Quantity", "FIFO_Flag"
    ]
    for col in expected_columns:
        if col not in inventory_df.columns:
            errors.append(f"Missing column: {col}")

    # Storage_ID uniqueness
    if not inventory_df["Storage_ID"].is_unique:
        errors.append("Duplicate Storage_IDs found")

    # Product_ID exists in products
    unknown_products = set(inventory_df["Product_ID"]) - set(products_df["Product_ID"])
    if unknown_products:
        errors.append(f"Unknown Product_IDs: {unknown_products}")

    # Stored_Quantity must be >= 0
    if (inventory_df["Stored_Quantity"] < 0).any():
        errors.append("Negative Stored_Quantity found")

    # FIFO_Flag must be 0 or 1
    if not inventory_df["FIFO_Flag"].isin([0, 1]).all():
        errors.append("Invalid FIFO_Flag (only 0 or 1 allowed)")

    # Zone and Rack_Location must not be null
    if inventory_df["Zone"].isnull().any():
        errors.append("Zone column contains null values")
    if inventory_df["Rack_Location"].isnull().any():
        errors.append("Rack_Location column contains null values")

    # Sum of stored quantity must not exceed available quantity in products
    grouped = inventory_df.groupby("Product_ID")["Stored_Quantity"].sum()
    for pid, stored_qty in grouped.items():
        available_qty = products_df.loc[products_df["Product_ID"] == pid, "Quantity_Available"].sum()
        if stored_qty > available_qty:
            errors.append(f"Stored quantity exceeds available for Product_ID {pid}")

    return errors

# Run validation
validation_errors = validate_inventory_against_products(df_products, df_inventory)

# Log output
if validation_errors:
    print("❌ Validation FAILED:")
    for err in validation_errors:
        print("-", err)
else:
    print("✅ All validations passed")

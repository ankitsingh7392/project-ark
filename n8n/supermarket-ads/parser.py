import os
from pathlib import Path

import pandas as pd

file_path = os.getenv("PRODUCT_XLSX_PATH", str(Path(__file__).parent / "product.xlsx"))

# Read header from 3rd row (0-based index = 2)
df = pd.read_excel(file_path, sheet_name="Stock Summary", header=2)
df = df.dropna(axis=1, how="all")
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.replace("\n", " ", regex=False)
    .str.replace("\t", " ", regex=False)
    .str.lower()
    .str.replace(" ", "_")
)

df = df.rename(columns={
    "item_code": "item_code",
    "selling_price": "selling_price",

})

# Keep only useful columns if present
wanted = [
    "item_code", "category", "brand", "name",
    "mrp", "selling_price", "qty", "status"
]
df = df[[c for c in wanted if c in df.columns]]

# Convert numerics
for col in ["mrp", "selling_price", "qty"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Clean text
for col in ["category", "brand", "name", "status", "show_online"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# Filter active and in-stock
if "status" in df.columns:
    df = df[df["status"].str.lower() == "active"]

if "qty" in df.columns:
    df = df[df["qty"].fillna(0) > 0]

df = df.dropna(subset=["name", "mrp", "selling_price"], how="any")

print(df.to_json(orient="records", force_ascii=False))

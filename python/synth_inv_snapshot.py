import random
from datetime import datetime, timedelta
import csv

# -----------------------------
# Configuration
# -----------------------------
OUTPUT_FILE = "pharma_inventory_lots_2025_2030.csv"
LOTS_PER_SKU = (7, 10)  # min and max lots per SKU

# -----------------------------
# SKU Master (from sales data)
# -----------------------------
SKUS = [
    ("772941PHM", "Amoxicillin 500mg Capsules"),
    ("884210PHM", "Metformin HCl 1000mg Tablets"),
    ("661550PHM", "Lisinopril 20mg Tablets"),
    ("992144PHM", "Atorvastatin 40mg Tablets"),
    ("450229PHM", "Ibuprofen 200mg Tablets"),
    ("773804PHM", "Insulin Glargine 100 units/mL Injection"),
    ("118920PHM", "Levothyroxine 75mcg Tablets"),
    ("994501PHM", "Omeprazole 20mg Capsules"),
    ("662118PHM", "Azithromycin 250mg Tablets"),
    ("552199PHM", "Losartan Potassium 50mg Tablets"),
    ("310447PHM", "Hydrochlorothiazide 25mg Tablets"),
    ("785332PHM", "Albuterol Sulfate Inhalation Aerosol"),
    ("669801PHM", "Sertraline 50mg Tablets"),
    ("441209PHM", "Prednisone 10mg Tablets"),
    ("903118PHM", "Warfarin Sodium 5mg Tablets")
]

# -----------------------------
# Helper Functions
# -----------------------------

def generate_lot():
    """Generate a random alphanumeric lot."""
    return f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(10,99)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100,999)}"

def generate_inventory_status():
    return random.choices(["Available", "Unreleased"], weights=[0.7, 0.3])[0]

def generate_inventory_qty():
    # realistic inventory qty (1,000 – 15,000 for solids, 500–2,500 for injectables)
    return random.randint(500, 15000)

def generate_expiration_date(sku_desc):
    """Generate realistic expiration date after 02/01/2027."""
    base_date = datetime(2027, 2, 2)
    if "Injection" in sku_desc or "Inhalation" in sku_desc:
        # injectables: 2–4 years shelf life
        delta_years = random.randint(2, 4)
    else:
        # oral solids: 3–5 years shelf life
        delta_years = random.randint(3, 5)
    year = base_date.year + delta_years
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # keep simple
    return datetime(year, month, day).strftime("%m/%d/%Y")

# -----------------------------
# Generate Inventory Data
# -----------------------------

inventory_rows = []

for sku, desc in SKUS:
    num_lots = random.randint(*LOTS_PER_SKU)
    for _ in range(num_lots):
        lot = generate_lot()
        status = generate_inventory_status()
        qty = generate_inventory_qty()
        exp_date = generate_expiration_date(desc)

        inventory_rows.append([
            sku,
            desc,
            lot,
            status,
            qty,
            exp_date
        ])

# -----------------------------
# Optional: Print Table Preview
# -----------------------------
print(f"{'SKU':<10} {'Description':<40} {'Lot':<10} {'Status':<12} {'Qty':<8} {'Expiration':<12}")
print("-"*95)
for row in inventory_rows[:20]:  # preview first 20 rows
    print(f"{row[0]:<10} {row[1]:<40} {row[2]:<10} {row[3]:<12} {row[4]:<8} {row[5]:<12}")

# -----------------------------
# Optional: Write CSV
# -----------------------------
with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["SKU", "SKU Description", "Lot", "Inventory Status", "Inventory Qty", "Expiration Date"])
    writer.writerows(inventory_rows)

print(f"\nInventory CSV generated: {OUTPUT_FILE}")

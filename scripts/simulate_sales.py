import csv
import random
import os
from datetime import datetime

DATA_DIR = "/opt/airflow/data"
FILE_PATH = os.path.join(DATA_DIR, "sales.csv")  # <--- Le CSV garde son nom standard

PRODUCTS = [
    ("PROD_LAPTOP", 999.99),
    ("PROD_MOUSE", 25.50),
    ("PROD_KEYBOARD", 75.00),
    ("PROD_MONITOR", 249.99),
    ("PROD_HEADSET", 50.00),
]

STORES = ["Store_Paris", "Store_Lyon", "Store_Marseille", "Online_Shop"]

def generate_data(num_rows=50):
    os.makedirs(DATA_DIR, exist_ok=True)
    
    with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["transaction_id", "timestamp", "store", "product_id", "quantity", "price"])
        
        for i in range(1, num_rows + 1):
            prod_id, base_price = random.choice(PRODUCTS)
            quantity = random.randint(1, 5)
            price = round(base_price * random.uniform(0.9, 1.0), 2)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            store = random.choice(STORES)
            
            writer.writerow([f"TXN_{i:04d}", timestamp, store, prod_id, quantity, price])
            
    print(f"✅ {num_rows} ventes générées dans : {FILE_PATH}")

if __name__ == "__main__":
    generate_data()
import pandas as pd
from sqlalchemy import create_engine

# Read the payment CSV
df = pd.read_csv("data/raw/olist_order_payments_dataset.csv")

# Connect to PostgreSQL
engine = create_engine(
    "postgresql+psycopg2://postgres:Ashreen1126@localhost:5432/customer_retention"
)

# Import payment data into PostgreSQL
df.to_sql(
    "order_payments",
    engine,
    if_exists="append",
    index=False
)

print("Order payments imported successfully!")
import pandas as pd
from sqlalchemy import create_engine

# Read order items CSV
df = pd.read_csv("data/raw/olist_order_items_dataset.csv")

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:Ashreen_1126@localhost:5432/customer_retention"
)

# Import data into PostgreSQL
df.to_sql(
    "order_items",
    engine,
    if_exists="append",
    index=False
)

print("Order items imported successfully!")
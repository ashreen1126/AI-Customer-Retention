import pandas as pd
from sqlalchemy import create_engine

# Read the customers CSV file
df = pd.read_csv("data/raw/olist_customers_dataset.csv")

# Create PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:Ashreen_1126@localhost:5432/customer_retention"
)

# Import data into PostgreSQL
df.to_sql("customers", engine, if_exists="append", index=False)

print("Customers imported successfully!")
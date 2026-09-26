import pandas as pd
from sqlalchemy import create_engine

# Read products CSV
df = pd.read_csv("data/raw/olist_products_dataset.csv")

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:Ashreen_1126@localhost:5432/customer_retention"
)

# Import data into PostgreSQL
df.to_sql(
    "products",
    engine,
    if_exists="append",
    index=False
)

print("Products imported successfully!")
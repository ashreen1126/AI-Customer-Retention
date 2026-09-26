import pandas as pd
from sqlalchemy import create_engine

# Read sellers CSV
df = pd.read_csv("data/raw/olist_sellers_dataset.csv")

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:Ashreen_1126@localhost:5432/customer_retention"
)

# Import sellers into PostgreSQL
df.to_sql(
    "sellers",
    engine,
    if_exists="append",
    index=False
)

print("Sellers imported successfully!")
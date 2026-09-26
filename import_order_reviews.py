import pandas as pd
from sqlalchemy import create_engine

# Read reviews CSV
df = pd.read_csv(
    "data/raw/olist_order_reviews_dataset.csv"
)

print("Total rows in CSV:", len(df))

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:Ashreen_1126@localhost:5432/customer_retention"
)

# Import reviews into PostgreSQL
df.to_sql(
    "order_reviews",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000
)

print("Order reviews imported successfully!")
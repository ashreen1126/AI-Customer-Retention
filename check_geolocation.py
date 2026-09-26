import pandas as pd
from sqlalchemy import create_engine

# Load geolocation CSV
df = pd.read_csv(
    "data/raw/olist_geolocation_dataset.csv"
)

print("Total rows:", len(df))
print("Columns:", df.columns.tolist())

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:Ashreen_1126@localhost:5432/customer_retention"
)

# Import into PostgreSQL
df.to_sql(
    "geolocation",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000
)

print("Geolocation data imported successfully!")
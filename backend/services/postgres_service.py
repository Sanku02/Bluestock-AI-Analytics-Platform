from sqlalchemy import create_engine
import pandas as pd


import os

DB_URL = (
    f"postgresql://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DB_URL)


def read_table(query: str):

    return pd.read_sql(query, engine)


def write_dataframe(
    df,
    table_name,
    if_exists="replace"
):

   df.to_sql(
    table_name,
    engine,
    schema="public",
    if_exists=if_exists,
    index=False
)
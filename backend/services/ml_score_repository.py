from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime


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


# ----------------------------------
# UPDATE LATEST SCORES
# ----------------------------------

def update_latest_scores(df):

    latest_df = df[
        [
            "symbol",
            "health_score",
            "rating"
        ]
    ].copy()

    latest_df["computed_at"] = datetime.now()

    latest_df.to_sql(

        "fact_ml_scores_latest",

        engine,

        if_exists="replace",

        index=False

    )


# ----------------------------------
# APPEND HISTORICAL SCORES
# ----------------------------------

def append_historical_scores(df):

    history_df = df[
        [
            "symbol",
            "health_score",
            "rating"
        ]
    ].copy()

    history_df["computed_at"] = datetime.now()

    history_df.to_sql(

        "fact_ml_scores",

        engine,

        if_exists="append",

        index=False

    )
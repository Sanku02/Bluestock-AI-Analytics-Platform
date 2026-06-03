from services.postgres_service import read_table

import services.scoring_service as scoring_service

from services.ml_score_repository import (
    update_latest_scores,
    append_historical_scores
)

import pandas as pd


def run_health_score_pipeline():

    query = """

    SELECT

        symbol,
        profit_margin,
        opm,
        de_ratio,
        cash_flow_ratio,
        investment_intensity,
        growth_proxy

    FROM fact_company_features

    """

    df = read_table(query)

    print(scoring_service.__file__)

    scored_df = scoring_service.compute_health_score(df)

    # ---------------------------------
    # PERSIST SCORES
    # ---------------------------------

    update_latest_scores(scored_df)

    append_historical_scores(scored_df)

    print(

        scored_df[
            [
                "symbol",
                "health_score",
                "rating"
            ]
        ].head()

    )

    return scored_df
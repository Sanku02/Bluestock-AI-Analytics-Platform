import pandas as pd
import numpy as np

print("SCORING SERVICE VERSION 2 LOADED")

# --------------------------------
# PERCENTILE NORMALIZATION
# --------------------------------

def percentile_score(series):

    series = series.fillna(0)

    return (
        series.rank(pct=True) * 100
    )


# --------------------------------
# REVERSE SCORE
# LOWER IS BETTER
# --------------------------------

def reverse_percentile_score(series):

    return 100 - percentile_score(series)


# --------------------------------
# LABELS
# --------------------------------

def assign_health_label(score):

    if score >= 85:
        return "EXCELLENT"

    elif score >= 70:
        return "GOOD"

    elif score >= 50:
        return "AVERAGE"

    elif score >= 35:
        return "WEAK"

    else:
        return "POOR"


# --------------------------------
# MAIN SCORING ENGINE
# --------------------------------

def compute_health_score(df):
    print("NEW HEALTH ENGINE RUNNING")

    # --------------------------------
    # FACTOR SCORES
    # --------------------------------

    df["profitability_score"] = (

        percentile_score(df["profit_margin"]) * 0.4

        +

        percentile_score(df["opm"]) * 0.6

    )

    df["growth_score"] = percentile_score(
        df["growth_proxy"]
    )

    df["cashflow_score"] = percentile_score(
        df["cash_flow_ratio"]
    )

    df["leverage_score"] = reverse_percentile_score(
        df["de_ratio"]
    )

    df["investment_score"] = reverse_percentile_score(
        df["investment_intensity"]
    )

    # --------------------------------
    # COMPOSITE SCORE
    # --------------------------------

    df["raw_health_score"] = (

        df["profitability_score"] * 0.30

        +

        df["growth_score"] * 0.25

        +

        df["leverage_score"] * 0.20

        +

        df["cashflow_score"] * 0.15

        +

        df["investment_score"] * 0.10

    )

    # --------------------------------
    # Z-SCORE STANDARDIZATION
    # --------------------------------

    mean_score = df["raw_health_score"].mean()

    std_score = df["raw_health_score"].std()

    df["z_score"] = (

        df["raw_health_score"] - mean_score

    ) / std_score

    # --------------------------------
    # CONVERT TO 0-100 SCALE
    # --------------------------------

    df["health_score"] = (

        50 + (df["z_score"] * 15)

    )

    # --------------------------------
    # CLIP TO RANGE
    # --------------------------------

    df["health_score"] = (

        df["health_score"]

        .clip(lower=0, upper=100)

    )

    print(df[
    [
        "profitability_score",
        "growth_score",
        "cashflow_score",
        "leverage_score",
        "investment_score",
        "health_score"
    ]
].head())

    # --------------------------------
    # LABELS
    # --------------------------------

    df["rating"] = df[
        "health_score"
    ].apply(assign_health_label)

    return df


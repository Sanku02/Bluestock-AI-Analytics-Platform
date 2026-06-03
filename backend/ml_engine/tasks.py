from celery import shared_task

from pipelines.scoring.health_score_pipeline import (
    run_health_score_pipeline
)


@shared_task
def nightly_health_refresh():

    print("Starting health score pipeline")

    df = run_health_score_pipeline()

    print("Pipeline completed")

    return f"Processed {len(df)} companies"
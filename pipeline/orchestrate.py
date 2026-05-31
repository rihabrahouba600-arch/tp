from dagster import job, op
import os

@op
def ingest():
    exit_code = os.system("python pipeline/ingest.py")
    if exit_code != 0:
        raise RuntimeError("L'ingestion a échoué.")

@op
def validate(context, ingest_input=None):
    exit_code = os.system("python pipeline/validate.py")
    if exit_code != 0:
        raise RuntimeError("La validation des données a échoué.")

@op
def transform(context, validate_input=None):
    exit_code = os.system("cd dbt_pipeline && dbt run --profiles-dir .")
    if exit_code != 0:
        raise RuntimeError("La transformation dbt a échoué.")

@op
def test_data(context, transform_input=None):
    exit_code = os.system("cd dbt_pipeline && dbt test --profiles-dir .")
    if exit_code != 0:
        raise RuntimeError("Les tests dbt ont échoué.")

@job
def ventes_pipeline():
    test_data(transform(validate(ingest())))
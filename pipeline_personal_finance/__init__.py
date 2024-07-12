import os
from dagster import Definitions, EnvVar
from dotenv import load_dotenv

from .resources import SqlAlchemyClientResource
from .assets import upload_dataframe_to_database

load_dotenv()

resources = {
    "prod": {
        "personal_finance_database": SqlAlchemyClientResource(
            drivername="postgresql+psycopg2",
            username=EnvVar("DAGSTER_POSTGRES_USER"),
            password=EnvVar("DAGSTER_POSTGRES_PASSWORD"),
            host=EnvVar("DAGSTER_POSTGRES_HOST"),
            port=int(os.getenv("DAGSTER_POSTGRES_PORT")),
            database=EnvVar("DAGSTER_POSTGRES_DB"),
            ),
    },
}

deployment_name = os.getenv("DAGSTER_DEPLOYMENT", "prod")

defs = Definitions(
    assets=[upload_dataframe_to_database],
    resources=resources[deployment_name],
)

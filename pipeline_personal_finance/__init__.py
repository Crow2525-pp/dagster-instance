import os

from dagster import Definitions, EnvVar
from dotenv import load_dotenv

from .resources import SqlAlchemyClientResource

# from dagster_duckdb import DuckDBResource

from .assets import upload_dataframe_to_database

load_dotenv()

# from .constants import DBT_PROJECT_DIR

from sqlalchemy import URL

resources = {
    # "dev": {
    #     "personal_finance_database": SqlAlchemyClientResource(
    #         connection_string="duckdb:///duckdb/finance.duckdb"
    #     ),
    "prod": {
        "personal_finance_database": SqlAlchemyClientResource(
            connection_string=str(
                URL.create(
                    drivername="postgresql",
                    username=EnvVar("DAGSTER_POSTGRES_USER"),
                    password=EnvVar("DAGSTER_POSTGRES_PASSWORD"),
                    host=EnvVar("DAGSTER_POSTGRES_HOST"),
                    port=int(os.environ.get("DAGSTER_POSTGRES_PORT")),
                    database=EnvVar("DAGSTER_POSTGRES_DB"),
                )
            )
        )
    },
}
# }


deployment_name = os.getenv("DAGSTER_DEPLOYMENT", "prod")

defs = Definitions(
    assets=[upload_dataframe_to_database],
    resources=resources[deployment_name],
)

import os

from dagster import Definitions, EnvVar

from .resources import SqlAlchemyClientResource

# from dagster_duckdb import DuckDBResource

from .assets import upload_dataframe_to_database

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
                    username=EnvVar("POSTGRES_USERNAME"),
                    password=EnvVar("POSTGRES_PASSWORD"),
                    host=EnvVar("POSTGRES_HOST"),
                    port=int(os.getenv("POSTGRES_PORT")),
                    database=EnvVar("POSTGRES_DB"),
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

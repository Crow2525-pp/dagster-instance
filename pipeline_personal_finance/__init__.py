import logging
import os
from dagster import Definitions, EnvVar, get_dagster_logger, resource
from dotenv import load_dotenv
from sqlalchemy.engine import URL

from .resources import SqlAlchemyClientResource
from .assets import upload_dataframe_to_database

load_dotenv()

my_logger = get_dagster_logger()

# Ensure EnvVar values are properly fetched from the environment variables
conn_str = URL.create(
    drivername="postgresql",
    username=os.environ.get("DAGSTER_POSTGRES_USER"),
    password=os.environ.get("DAGSTER_POSTGRES_PASSWORD"),
    host=os.environ.get("DAGSTER_POSTGRES_HOST"),
    #port=int(os.environ.get("DAGSTER_POSTGRES_PORT")),
    database=os.environ.get("DAGSTER_POSTGRES_DB"),
)
my_logger.info(f"Connection string: {conn_str}")

@resource
def sqlalchemy_resource(context):
    connection_string = str(
        URL.create(
            drivername="postgresql",
            username=EnvVar("DAGSTER_POSTGRES_USER"),
            password=EnvVar("DAGSTER_POSTGRES_PASSWORD"),
            host=EnvVar("DAGSTER_POSTGRES_HOST"),
            #port=int(EnvVar("DAGSTER_POSTGRES_PORT")),
            database=EnvVar("DAGSTER_POSTGRES_DB"),
        )
    )
    context.log.info(f"Initializing SqlAlchemyClientResource with connection string: {connection_string}")
    return SqlAlchemyClientResource(connection_string=connection_string)

resources = {
    "prod": {
        "personal_finance_database": sqlalchemy_resource,
    },
}

deployment_name = os.getenv("DAGSTER_DEPLOYMENT", "prod")

defs = Definitions(
    assets=[upload_dataframe_to_database],
    resources=resources[deployment_name],
)

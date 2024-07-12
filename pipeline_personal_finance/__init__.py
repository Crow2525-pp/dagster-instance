import logging
import os
from dagster import Definitions, EnvVar, get_dagster_logger, resource
from dotenv import load_dotenv
from sqlalchemy.engine import URL

from .resources import SqlAlchemyClientResource
from .assets import upload_dataframe_to_database

load_dotenv()

my_logger = get_dagster_logger()

# # Debugging: Print environment variables to verify they are loaded
# my_logger.info(f"DAGSTER_POSTGRES_HOST: {EnvVar('DAGSTER_POSTGRES_HOST')}")
# my_logger.info(f"DAGSTER_POSTGRES_USER: {EnvVar('DAGSTER_POSTGRES_USER')}")
# my_logger.info(f"DAGSTER_POSTGRES_PASSWORD: {EnvVar('DAGSTER_POSTGRES_PASSWORD')}")
# my_logger.info(f"DAGSTER_POSTGRES_PORT: {EnvVar('DAGSTER_POSTGRES_PORT')}")
# my_logger.info(f"DAGSTER_POSTGRES_DB: {EnvVar('DAGSTER_POSTGRES_DB')}")

# Using standard Python logging
import logging
logger = logging.getLogger('dagster')

# Logging environment variable value directly after fetching it correctly
port = os.getenv("DAGSTER_POSTGRES_PORT")
port = int(port)

resources = {
    "prod": {
        "personal_finance_database": SqlAlchemyClientResource(
            drivername="postgresql+psycopg2",
            username=EnvVar("DAGSTER_POSTGRES_USER"),
            password=EnvVar("DAGSTER_POSTGRES_PASSWORD"),
            host=EnvVar("DAGSTER_POSTGRES_HOST"),
            #port=port,
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

# pipeline_personal_finance/resources.py

import sqlalchemy
from dagster import ConfigurableResource, InitResourceContext, EnvVar



class SqlAlchemyClientResource(ConfigurableResource):
    def __init__(self):
        self.drivername = "postgresql+psycopg2"
        self.username = EnvVar("DAGSTER_POSTGRES_USER")
        self.password = EnvVar("DAGSTER_POSTGRES_PASSWORD")
        self.host = EnvVar("DAGSTER_POSTGRES_HOST")
        self.port = EnvVar("DAGSTER_POSTGRES_PORT")
        self.database = EnvVar("DAGSTER_POSTGRES_DB")
        self.connection_string = self.get_connection_string()

    def get_connection_string(self):
        return str(
            sqlalchemy.URL.create(                
                drivername=self.drivername,
                username=self.username,
                password=self.password,
                host=self.host,
                port=int(self.port),
                database=self.database
            )
        )

    def create_engine(self):
        return sqlalchemy.create_engine(self.connection_string)

    def get_connection(self):
        return self.create_engine().connect()
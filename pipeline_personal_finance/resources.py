# pipeline_personal_finance/resources.py

import sqlalchemy
from dagster import ConfigurableResource


class SqlAlchemyClientResource(ConfigurableResource):
    connection_string: str

    def create_engine(self):
        return sqlalchemy.create_engine(self.connection_string)

    def get_connection(self):
        return self.create_engine().connect()
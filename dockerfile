FROM python:3.11-slim

# Environment variables
ENV DAGSTER_HOME=/docker/appdata/dagster/dagster_home/
ENV DAGSTER_APP=/docker/appdata/dagster

# Create application directory
RUN mkdir -p ${DAGSTER_APP}

# Install Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create true
COPY pyproject.toml poetry.lock ${DAGSTER_APP}/
WORKDIR ${DAGSTER_APP}

# Install dependencies with Poetry
RUN poetry install

# Initialize Poetry shell (optional, depending on your setup)
RUN poetry shell

# Create Dagster home directory
RUN mkdir -p ${DAGSTER_HOME}
COPY workspace.yml docker.yml ${DAGSTER_HOME}/

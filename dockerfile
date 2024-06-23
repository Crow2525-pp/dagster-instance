# ./dockerfile

FROM python:3.11-slim

# Environment variables
ENV DAGSTER_HOME=/docker/appdata/dagster/dagster_home/
ENV DAGSTER_APP=/docker/appdata/dagster

# Create application directory
WORKDIR ${DAGSTER_APP}

COPY requirements.txt pyproject.toml ./

# Install the required dependencies
RUN pip install -r requirements.txt
WORKDIR ${DAGSTER_APP}

# Create Dagster home directory
RUN mkdir -p ${DAGSTER_HOME}
COPY workspace.yaml docker.yaml  ${DAGSTER_HOME}/

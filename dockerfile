# ./dockerfile

FROM python:3.11-slim

# Environment variables
ENV DAGSTER_HOME=/docker/appdata/dagster/dagster_home/
ENV DAGSTER_APP=/docker/appdata/dagster

# Create application directory
RUN mkdir -p ${DAGSTER_APP}

COPY requirements.txt ./

# Install the required dependencies
RUN pip install -r requirements.txt
WORKDIR ${DAGSTER_APP}

# Create Dagster home directory
RUN mkdir -p ${DAGSTER_HOME}
COPY workspace.yml docker.yml ${DAGSTER_HOME}/

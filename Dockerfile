# Use the official Python image from the Docker Hub
FROM python:3.11-slim AS build

WORKDIR /build
ARG ENV
ARG VIRTUAL_ENV

# Copy the required file into container
COPY requirements/${ENV}.txt .
COPY src src
COPY setup.py .

# Create and activate the virtual environment, then install dependencies
RUN python -m venv ${VIRTUAL_ENV} && \
    ${VIRTUAL_ENV}/bin/pip install --upgrade pip && \
    ${VIRTUAL_ENV}/bin/pip install --no-cache-dir -r ${ENV}.txt && \
    ${VIRTUAL_ENV}/bin/pip install .

# Copy the rest of the application code into the container
FROM python:3.11-slim AS runtime

WORKDIR /app
ARG VIRTUAL_ENV
ENV PYTHON=/app/${VIRTUAL_ENV}/bin/python

COPY --from=build /build/${VIRTUAL_ENV} ${VIRTUAL_ENV}

EXPOSE 5000

RUN mkdir etc
COPY startup.sh .

# Run the startup script
CMD ["sh", "-c", "./startup.sh ${PYTHON}"]

# null CMD for debugging
# CMD ["tail", "-f", "/dev/null"]

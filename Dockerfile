
FROM python:3.9-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

# Copy local code to the container image.
COPY . ./

RUN apt-get update && apt-get -y upgrade
RUN apt-get update \
    && apt-get -y install curl libpq-dev gcc \
    && pip install psycopg2
RUN apt-get update && apt-get install -y gdal-bin

# Allow statements and log 
ENV PYTHONUNBUFFERED True

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install production dependencies using Poetry
RUN pip install --no-cache-dir poetry && poetry install --no-root --no-dev

# Instalar FastAPI
RUN pip install fastapi
RUN pip install httpx
RUN pip install pydantic
RUN pip install python-multipart

# Install uvicorn
RUN pip install uvicorn

ENV PORT 5000
# Expose the port on which your Python app runs (if needed)
EXPOSE 5000

# Run
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
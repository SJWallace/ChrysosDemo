FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install confluent-kafka psycopg2-binary

# Create directories
RUN mkdir -p /app/producer /app/consumer

# Copy files instead of mounting volumes
COPY ./producer /app/producer
COPY ./consumer /app/consumer

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command (will be overridden in docker-compose)
CMD ["python", "app.py"]

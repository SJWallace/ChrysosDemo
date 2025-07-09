FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install confluent-kafka psycopg2-binary

# Copy application code
COPY ./ /app/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command (will be overridden in docker-compose)
CMD ["python", "app.py"]
from confluent_kafka import Consumer
import psycopg2, json, os
import time

# Wait for Kafka to be ready
time.sleep(10)

c = Consumer({
    'bootstrap.servers': 'kafka:9092',  # Updated to use service name
    'group.id': 'demo', 
    'auto.offset.reset': 'earliest'
})
c.subscribe(['sensor_readings'])

# Retry connection to PostgreSQL
max_retries = 5
retry_count = 0
while retry_count < max_retries:
    try:
        conn = psycopg2.connect(
            dbname="chrysosdemo", 
            user="chrysosdemo", 
            password=os.environ.get('POSTGRES_PASSWORD'), 
            host="postgres",  # Updated to use service name
            port="5432"  # Updated to use default port
        )
        break
    except psycopg2.OperationalError:
        retry_count += 1
        print(f"Connection attempt {retry_count} failed. Retrying in 5 seconds...")
        time.sleep(5)

if retry_count == max_retries:
    raise Exception("Failed to connect to PostgreSQL after multiple attempts")

cur = conn.cursor()
print("Kafka consumer started. Waiting for messages...")

while True:
    msg = c.poll(1.0)
    if msg is None or msg.error():
        continue
    data = json.loads(msg.value())
    print(f"Received data: {data}")
    cur.execute("INSERT INTO raw_sensor_data (sensor_id, timestamp, temperature) VALUES (%s, to_timestamp(%s), %s)",
                (data['sensor_id'], data['timestamp'], data['temperature']))
    conn.commit()
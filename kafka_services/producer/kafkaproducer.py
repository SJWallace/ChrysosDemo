from confluent_kafka import Producer
import random, time, json

# Wait for Kafka to be ready
time.sleep(10)

p = Producer({'bootstrap.servers': 'kafka:9092'})  # Updated to use service name
print("Kafka producer started. Generating sensor data...")

while True:
    reading = {
        "sensor_id": random.randint(1, 5),
        "timestamp": int(time.time()),
        "temperature": round(random.uniform(15, 30), 2)
    }
    print(f"Producing data: {reading}")
    p.produce('sensor_readings', value=json.dumps(reading))
    p.flush()
    time.sleep(1)
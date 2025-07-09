from confluent_kafka import Consumer
import psycopg2, json, os
import time
from psycopg2 import errors

# Wait for Kafka to be ready
time.sleep(10)

c = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'photon_assay_demo',
    'auto.offset.reset': 'earliest'
})
c.subscribe(['photon_assay_data'])

# Retry connection to PostgreSQL
max_retries = 5
retry_count = 0
while retry_count < max_retries:
    try:
        conn = psycopg2.connect(
            dbname="chrysosdemo", 
            user="chrysosdemo", 
            password=os.environ.get('POSTGRES_PASSWORD'), 
            host="postgres",
            port="5432"
        )
        break
    except psycopg2.OperationalError:
        retry_count += 1
        print(f"Connection attempt {retry_count} failed. Retrying in 5 seconds...")
        time.sleep(5)

if retry_count == max_retries:
    raise Exception("Failed to connect to PostgreSQL after multiple attempts")

cur = conn.cursor()
print("Photon Assay Kafka consumer started. Waiting for messages...")

while True:
    msg = c.poll(1.0)
    if msg is None or msg.error():
        continue

    data = json.loads(msg.value())
    print(f"Received photon assay data: {data}")

    try:
        # Insert into photon_assay_events table
        cur.execute(
            "INSERT INTO photon_assay_events (assay_id, timestamp, status) VALUES (%s, %s, %s)",
            (data['assay_id'], data['timestamp'], data['status'])
        )

        # Insert or update device information
        cur.execute(
            """
            INSERT INTO photon_assay_devices 
            (device_id, device_type, location, calibration_date, firmware_version, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (device_id) DO UPDATE SET
            device_type = EXCLUDED.device_type,
            location = EXCLUDED.location,
            calibration_date = EXCLUDED.calibration_date,
            firmware_version = EXCLUDED.firmware_version,
            status = EXCLUDED.status
            """,
            (
                data['device']['device_id'],
                data['device']['device_type'],
                data['device']['location'],
                data['device']['calibration_date'],
                data['device']['firmware_version'],
                data['device']['status']
            )
        )

        # Map assay to device
        cur.execute(
            "INSERT INTO photon_assay_device_mapping (assay_id, timestamp, device_id) VALUES (%s, %s, %s)",
            (data['assay_id'], data['timestamp'], data['device']['device_id'])
        )

        # Insert spectrum data
        for i, energy in enumerate(data['spectrum']['energy_keV']):
            intensity = data['spectrum']['intensity'][i]
            cur.execute(
                "INSERT INTO photon_assay_spectra (assay_id, timestamp, energy_kev, intensity) VALUES (%s, %s, %s, %s)",
                (data['assay_id'], data['timestamp'], energy, intensity)
            )

        conn.commit()

    except errors.UniqueViolation as e:
        conn.rollback()  # Roll back the transaction
        print(f"Skipping duplicate assay_id: {data['assay_id']}. Error: {e}")
    except Exception as e:
        conn.rollback()  # Roll back the transaction
        print(f"Error processing message: {e}")

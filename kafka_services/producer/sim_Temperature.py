from confluent_kafka import Producer
import random, time, json
import math
from datetime import datetime

# Wait for Kafka to be ready
time.sleep(10)

p = Producer({'bootstrap.servers': 'kafka:9092'})  # Updated to use service name
print("Kafka producer started. Generating sensor data with cyclic weather patterns...")

# Temperature parameters
BASE_TEMP = 22.5  # Base temperature (average between 15 and 30)
TEMP_AMPLITUDE = 7.5  # Amplitude of temperature variation (half of the range 15-30)
RANDOM_VARIATION = 1.5  # Random variation to add realism

def get_cyclic_temperature():
    # Get current hour and minute
    now = datetime.now()
    hour = now.hour
    minute = now.minute

    # Convert to hour fraction (0-24 range)
    hour_fraction = hour + minute / 60.0

    # Calculate where we are in the daily cycle
    # Coolest at 5 AM, warmest at 3 PM (15:00)
    # Shift the sine wave to match this pattern
    phase_shift = 5  # 5 AM is the coolest point
    cycle_position = (hour_fraction - phase_shift) * (2 * math.pi / 24)

    # Calculate temperature using a sine wave
    # sin() returns -1 to 1, so we scale and shift it to our temperature range
    temperature = BASE_TEMP + TEMP_AMPLITUDE * math.sin(cycle_position)

    # Add some random variation to make it more realistic
    temperature += random.uniform(-RANDOM_VARIATION, RANDOM_VARIATION)

    return round(temperature, 2)

while True:
    current_temp = get_cyclic_temperature()

    reading = {
        "sensor_id": random.randint(1, 5),
        "timestamp": int(time.time()),
        "temperature": current_temp
    }
    print(f"Producing data: {reading}")
    p.produce('sensor_readings', value=json.dumps(reading))
    p.flush()
    time.sleep(1)

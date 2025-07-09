import random, time, json
from datetime import datetime, timedelta
from confluent_kafka import Producer
import uuid

DEVICE_INFO = {
    "device_id": "CHRYSOS001",
    "device_type": "PhotonAssay9000",
    "location": "Site Alpha",
    "calibration_date": (datetime.now() - timedelta(days=random.randint(0,60))).strftime('%Y-%m-%d'),
    "firmware_version": "1.2.3",
    "status": "operational"
}

ENERGY_BINS = [round(1.0 + 0.1*i, 1) for i in range(0, 391)]  # 1.0 to 40.0 keV in 0.1 steps

def generate_spectrum():
    # Simulate a Gaussian-like peak
    peak_energy = random.uniform(5, 30)
    peak_height = random.uniform(100, 2000)
    width = random.uniform(0.5, 2.0)
    spectrum = []
    for e in ENERGY_BINS:
        intensity = (
            peak_height *
            (1 / (width * (2 * 3.14159)**0.5)) *
            pow(2.71828, -0.5 * ((e - peak_energy) / width) ** 2)
        )
        intensity += random.uniform(0, 5)  # noise
        spectrum.append(int(round(intensity)))
    return spectrum

p = Producer({'bootstrap.servers': 'kafka:9092'})

def send_instrument_packet():
    data = {
        "assay_id": f"ASSAY{uuid.uuid4().hex[:8].upper()}",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "device": DEVICE_INFO,
        "spectrum": {
            "energy_keV": ENERGY_BINS,
            "intensity": generate_spectrum()
        },
        "status": random.choices(["ok", "warning", "fail"], [0.98, 0.01, 0.01])[0]
    }
    p.produce('photon_assay_data', value=json.dumps(data))
    print(f"Sent: assay_id={data['assay_id']} status={data['status']}")

if __name__ == "__main__":
    while True:
        send_instrument_packet()
        p.flush()
        time.sleep(random.uniform(60, 180))

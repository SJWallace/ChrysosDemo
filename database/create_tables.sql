CREATE TABLE IF NOT EXISTS raw_sensor_data (
    sensor_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperature DOUBLE PRECISION
);

-- Table for storing assay events
CREATE TABLE IF NOT EXISTS photon_assay_events (
    assay_id TEXT PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('ok', 'warning', 'fail'))
);

-- Table for storing device information
CREATE TABLE IF NOT EXISTS photon_assay_devices (
    device_id TEXT PRIMARY KEY,
    device_type TEXT NOT NULL,
    location TEXT,
    calibration_date DATE,
    firmware_version TEXT,
    status TEXT
);

-- Table for storing the relationship between assays and devices
CREATE TABLE IF NOT EXISTS photon_assay_device_mapping (
    assay_id TEXT REFERENCES photon_assay_events(assay_id),
    device_id TEXT REFERENCES photon_assay_devices(device_id),
    PRIMARY KEY (assay_id, device_id)
);

-- Table for storing spectrum data
CREATE TABLE IF NOT EXISTS photon_assay_spectra (
    assay_id TEXT REFERENCES photon_assay_events(assay_id),
    energy_kev DOUBLE PRECISION NOT NULL,
    intensity INTEGER NOT NULL,
    PRIMARY KEY (assay_id, energy_kev)
);

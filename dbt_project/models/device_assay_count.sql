SELECT
  d.device_id,
  d.location,
  COUNT(DISTINCT m.assay_id) AS assays_run
FROM photon_assay_device_mapping m
JOIN photon_assay_devices d ON m.device_id = d.device_id
GROUP BY d.device_id, d.location

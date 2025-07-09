-- Photon Assay Daily Report
-- This model provides a simple daily report of photon assay activity

SELECT
    date_trunc('day', e.timestamp) AS day,
    e.status,
    COUNT(*) AS assay_count,
    COUNT(DISTINCT d.device_id) AS devices_used,
    STRING_AGG(DISTINCT d.location, ', ') AS locations
FROM {{ source('public', 'photon_assay_events') }} e
JOIN {{ source('public', 'photon_assay_device_mapping') }} m ON e.assay_id = m.assay_id
JOIN {{ source('public', 'photon_assay_devices') }} d ON m.device_id = d.device_id
GROUP BY day, e.status
ORDER BY day DESC, e.status
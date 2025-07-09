-- Photon Assay Analytics Model
-- This model provides analytics on photon assay data

WITH assay_stats AS (
    -- Get basic statistics about assays by status
    SELECT
        date_trunc('day', timestamp) AS day,
        status,
        COUNT(*) AS assay_count
    FROM {{ source('public', 'photon_assay_events') }}
    GROUP BY day, status
),

device_stats AS (
    -- Get statistics about devices and their usage
    SELECT
        d.device_id,
        d.device_type,
        d.location,
        COUNT(m.assay_id) AS total_assays,
        MAX(e.timestamp) AS last_used
    FROM {{ source('public', 'photon_assay_devices') }} d
    LEFT JOIN {{ source('public', 'photon_assay_device_mapping') }} m ON d.device_id = m.device_id
    LEFT JOIN {{ source('public', 'photon_assay_events') }} e ON m.assay_id = e.assay_id
    GROUP BY d.device_id, d.device_type, d.location
),

spectrum_stats AS (
    -- Get statistics about spectrum data
    SELECT
        s.assay_id,
        AVG(s.energy_kev) AS avg_energy,
        MAX(s.energy_kev) AS max_energy,
        MIN(s.energy_kev) AS min_energy,
        AVG(s.intensity) AS avg_intensity,
        MAX(s.intensity) AS max_intensity
    FROM {{ source('public', 'photon_assay_spectra') }} s
    GROUP BY s.assay_id
)

-- Final combined analytics
SELECT
    a.day,
    a.status,
    a.assay_count,
    d.device_id,
    d.device_type,
    d.location,
    d.total_assays,
    d.last_used,
    s.avg_energy,
    s.max_energy,
    s.min_energy,
    s.avg_intensity,
    s.max_intensity
FROM assay_stats a
CROSS JOIN device_stats d
LEFT JOIN spectrum_stats s ON TRUE
ORDER BY a.day DESC, d.total_assays DESC
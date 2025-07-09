-- Photon Assay Spectrum Analysis
-- This model provides detailed analysis of spectrum data from photon assays

WITH spectrum_bins AS (
    -- Create energy bins for analysis
    SELECT
        assay_id,
        CASE
            WHEN energy_kev < 100 THEN 'Low (<100 keV)'
            WHEN energy_kev >= 100 AND energy_kev < 500 THEN 'Medium (100-500 keV)'
            WHEN energy_kev >= 500 AND energy_kev < 1000 THEN 'High (500-1000 keV)'
            ELSE 'Very High (>1000 keV)'
        END AS energy_range,
        energy_kev,
        intensity
    FROM {{ source('public', 'photon_assay_spectra') }}
),

assay_device_info AS (
    -- Join assay and device information
    SELECT
        e.assay_id,
        e.timestamp,
        e.status,
        d.device_id,
        d.device_type,
        d.location
    FROM {{ source('public', 'photon_assay_events') }} e
    JOIN {{ source('public', 'photon_assay_device_mapping') }} m ON e.assay_id = m.assay_id
    JOIN {{ source('public', 'photon_assay_devices') }} d ON m.device_id = d.device_id
)

-- Final analysis combining spectrum data with assay and device information
SELECT
    a.assay_id,
    a.timestamp,
    a.status,
    a.device_id,
    a.device_type,
    a.location,
    s.energy_range,
    COUNT(*) AS measurement_count,
    AVG(s.energy_kev) AS avg_energy,
    AVG(s.intensity) AS avg_intensity,
    MAX(s.intensity) AS peak_intensity,
    SUM(s.intensity) AS total_intensity
FROM spectrum_bins s
JOIN assay_device_info a ON s.assay_id = a.assay_id
GROUP BY 
    a.assay_id,
    a.timestamp,
    a.status,
    a.device_id,
    a.device_type,
    a.location,
    s.energy_range
ORDER BY 
    a.timestamp DESC,
    a.assay_id,
    s.energy_range
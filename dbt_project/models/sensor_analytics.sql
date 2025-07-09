SELECT
  sensor_id,
  date_trunc('hour', timestamp) AS hour,
  avg(temperature) AS avg_temp
FROM {{ source('public', 'raw_sensor_data') }}
GROUP BY sensor_id, hour
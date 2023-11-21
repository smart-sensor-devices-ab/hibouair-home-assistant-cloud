#add this lines to configuration.yaml
sensor: 
    - platform: hibouair
    scan_interval: 120

#Sample Entities Card configuration
type: entities
entities:
  - entity: sensor.hibouair_co2
  - entity: sensor.hibouair_temperature
  - entity: sensor.hibouair_humidity
  - entity: sensor.hibouair_light
  - entity: sensor.hibouair_pm1
  - entity: sensor.hibouair_pm2_5
  - entity: sensor.hibouair_pm10
  - entity: sensor.hibouair_pressure
  - entity: sensor.hibouair_voc
  - entity: sensor.hibouair_last_updated
header:
  type: picture
  image: https://www.hibouair.com/blog/wp-content/uploads/2023/10/hibouair_banner.png
  tap_action:
    action: none
  hold_action:
    action: none



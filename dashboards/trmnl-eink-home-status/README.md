# TRMNL 800×480 E-Ink Home Status Dashboard

A fixed-size Home Assistant dashboard template designed for an **800×480 TRMNL e-ink display**. The dashboard is intended to be rendered by Home Assistant and captured as a static image by TRMNL HA.

> This is a **dashboard template**, not a native Home Assistant automation/script blueprint. Home Assistant does not currently provide a Blueprint import flow for dashboards, so installation is by copying the dashboard YAML and replacing the placeholder entities.

## Design goals

- Fit entirely inside a single 800×480 image
- Prioritize actionable notifications and current weather
- Keep security, indoor conditions, and outdoor air quality visible at a glance
- Use a static, non-interactive RainViewer radar optimized for e-ink capture
- Hide the normal Home Assistant header/sidebar when captured
- Keep normal states visually quiet while promoting urgent smoke, CO, or security alarms

## Layout

The template uses three columns across the top and three compact status panels along the bottom:

```text
┌──────────────────────────┬──────────────────┬──────────────────────────┐
│ NOTIFICATIONS            │ TODAY            │ RADAR                    │
│                          │                  │                          │
│ Active alerts            │ Temp             │ Static OSM / RainViewer │
│ Laundry                  │ Conditions       │ Home marker              │
│ Doors / vehicle / plants │ Rain probability │ Severe alerts            │
│ Safety alerts            │ Humidity / wind  │                          │
├──────────────────────────┼──────────────────┼──────────────────────────┤
│ SECURITY                 │ INDOOR           │ OUTSIDE AIR              │
│ Mode / alarm / locks     │ Temp / humidity  │ AQI / pollutants         │
│ Smoke/CO health          │ HVAC / PM2.5     │ Station temp / humidity  │
├──────────────────────────┴──────────────────┴──────────────────────────┤
│ Refreshed date/time                                                   │
└───────────────────────────────────────────────────────────────────────┘
```

## Requirements

The dashboard template uses the following Home Assistant frontend resources:

- **button-card**
- **layout-card**
- **Kiosk Mode**
- **weather-radar-card**

For TRMNL image delivery, use the **TRMNL HA** app/add-on or another screenshot workflow capable of rendering the dashboard at 800×480.

## Recommended TRMNL capture settings

- Dashboard path: your dedicated dashboard/view path
- Width: `800`
- Height: `480`
- Zoom: `1.0`
- Image format: `PNG`
- Render delay: about `3000 ms`
- Dark mode: off
- Cropping: off

If Kiosk Mode is enabled and you need the Home Assistant header back while editing, append:

```text
?disable_km
```

to the dashboard URL.

## Installation

1. Install the required frontend resources.
2. Create a dedicated Home Assistant dashboard.
3. Open **Edit dashboard → Raw configuration editor**.
4. Copy the contents of [`dashboard-template.yaml`](dashboard-template.yaml).
5. Replace every `replace_*` placeholder entity with the matching entity from your Home Assistant installation.
6. Save and reload the dashboard.
7. Configure TRMNL HA to capture the dedicated dashboard at 800×480.

## Entity placeholders

The template intentionally uses valid-looking but nonexistent Home Assistant entity IDs so the YAML can be pasted before customization.

### System and security

| Placeholder | Purpose |
| --- | --- |
| `input_select.replace_system_mode` | Household/system mode |
| `alarm_control_panel.replace_security_system` | Alarm state |
| `binary_sensor.replace_primary_door_contact` | Primary/front door open state |
| `binary_sensor.replace_secondary_door_contact` | Secondary door open state |
| `lock.replace_primary_door_lock` | Primary/front door lock |
| `lock.replace_vehicle_lock` | Vehicle lock |

### Vehicle notifications

| Placeholder | Purpose |
| --- | --- |
| `binary_sensor.replace_vehicle_engine` | Engine running |
| `binary_sensor.replace_vehicle_low_fuel` | Low-fuel warning |
| `binary_sensor.replace_vehicle_tire_pressure_all` | Aggregate tire-pressure warning |
| `binary_sensor.replace_vehicle_tire_pressure_front_left` | Front-left tire warning |
| `binary_sensor.replace_vehicle_tire_pressure_front_right` | Front-right tire warning |
| `binary_sensor.replace_vehicle_tire_pressure_rear_left` | Rear-left tire warning |
| `binary_sensor.replace_vehicle_tire_pressure_rear_right` | Rear-right tire warning |

### Laundry and plants

| Placeholder | Purpose |
| --- | --- |
| `sensor.replace_washer_cycle_status` | Expected states: `idle`, `running`, `complete` |
| `input_select.replace_dryer_cycle_status` | Expected states: `Idle`, `Running`, `Complete` |
| `sensor.replace_plant_moisture_minimum` | Aggregate/minimum plant moisture percentage |

The plant notification appears only below 25% and reads `Plants need watering (X%)`.

### Smoke / CO detector

| Placeholder | Purpose |
| --- | --- |
| `binary_sensor.replace_smoke_detected` | Smoke/fire alarm |
| `binary_sensor.replace_co_detected` | Carbon monoxide alarm |
| `binary_sensor.replace_detector_replace_battery_now` | Replace battery now |
| `binary_sensor.replace_detector_replace_battery_soon` | Replace battery soon |
| `binary_sensor.replace_detector_tamper` | Tamper/cover warning |
| `sensor.replace_detector_node_status` | Z-Wave/device health state |
| `sensor.replace_detector_battery_level` | Battery percentage |

The template treats `asleep` as a normal state for battery-powered Z-Wave detectors. `dead`, `offline`, `unknown`, or `unavailable` are promoted to the Notification Center.

### Weather and indoor climate

| Placeholder | Purpose |
| --- | --- |
| `weather.replace_weather` | Current weather entity |
| `sensor.replace_local_rain_probability_60m` | Local 60-minute rain probability |
| `sensor.replace_indoor_temperature` | Indoor temperature |
| `sensor.replace_indoor_humidity` | Indoor humidity |
| `climate.replace_thermostat` | Thermostat mode/action/set point |
| `sensor.replace_indoor_pm25_average` | Indoor PM2.5 average |

### Outdoor air quality

| Placeholder | Purpose |
| --- | --- |
| `sensor.replace_outdoor_aqi` | AQI |
| `sensor.replace_outdoor_dominant_pollutant` | Dominant pollutant |
| `sensor.replace_outdoor_pm25` | PM2.5 reading |
| `sensor.replace_outdoor_pm10` | PM10 reading |
| `sensor.replace_outdoor_temperature` | Outdoor/station temperature |
| `sensor.replace_outdoor_humidity` | Outdoor/station humidity |

## Radar configuration

The included radar is deliberately static and non-interactive for e-ink screenshot capture:

- RainViewer data
- OSM basemap
- Static map
- No playback, zoom, or recenter controls
- Scale and color bar enabled
- `zone.home` marker
- Severe weather alerts enabled
- Zoom level 9

Adjust the zoom level and marker entity as needed for your installation.

## Notification behavior

The Notification Center promotes only actionable or relevant states, including:

- Smoke / fire alarm
- Carbon monoxide alarm
- Triggered security alarm
- Smoke/CO detector communication or battery problems
- Open doors
- Jammed locks
- Vehicle engine running
- Low fuel
- Tire-pressure warnings
- Washer/dryer running or complete
- Plant moisture below 25%

When no notifications are active, the panel displays **All clear**.

## Customization

The layout is intentionally strict because responsive Home Assistant layouts can overflow or stack when captured at TRMNL dimensions. The key dimensions are:

```yaml
grid-template-columns: "2.7fr 1.9fr 2.7fr"
grid-template-rows: "292px 140px 16px"
```

If you change these values, validate the result in the TRMNL HA 800×480 preview before deploying it to the physical display.

## Repository note

This template is designed as a reusable starting point. Entity IDs are placeholders rather than values from a specific Home Assistant installation so the resource can be shared safely and adapted to other systems.

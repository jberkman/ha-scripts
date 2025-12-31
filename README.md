# ha-scripts — Generated Home Assistant Heating Logic

This repo contains a small toolchain that generates parts of my Home Assistant configuration from a single source of truth: `rooms.yaml`.

The goal is to avoid hand-maintaining room-specific helpers, thermostats, and logic — instead, I describe the rooms once, and the scripts generate the required HA YAML.

## What this system does

From `ha-scripts/rooms.yaml`, the generators produce:

### Per-room helpers

For each room (`id`, `label`):

- `input_boolean.<id>_active`
- `input_boolean.<id>_heat_request`

These represent whether the room is **occupied / in use** and whether the room **wants heat**.

### Virtual thermostats

For each room with a `temp_sensor`, a `generic_thermostat` is generated:

- `climate.<id>_thermostat`

This thermostat drives the room’s `<id>_heat_request` helper rather than a real heater — the real heating system is controlled elsewhere.

### Global master switch

Also generated:

- `input_boolean.heat_permitted`

If this is off, heating is globally disabled.

### Derived state — “Any Room Needs Heat”

A template `binary_sensor` is generated:

- `binary_sensor.any_room_needs_heat`

Its state is:

> `heat_permitted == on` **AND**  
> at least one room is **active** **and** **calling for heat**

This single sensor is exported to HomeKit and used to control the *real* thermostat there (because HomeKit automation logic is limited).

## File layout

These scripts generate YAML into standard HA include directories:

```
/config/input_booleans/ha-scripts.yaml
/config/climates/ha-scripts.yaml
/config/templates/ha-scripts.yaml
```

Home Assistant must have:

```yaml
input_boolean: !include_dir_merge_named input_booleans/
climate: !include_dir_merge_list climates/
template: !include_dir_merge_list templates/
```

## Source of truth: `rooms.yaml`

Example:

```yaml
- id: bedroom
  label: Bedroom
  temp_sensor: sensor.bedroom_awair_temperature

- id: away
  label: Away
  temp_sensor: sensor.bedroom_awair_temperature   # virtual mode for now
```

If a room is listed here, the rest of the config is generated automatically.

## Running the generator

From this repo:

```bash
./generate_all.py /path/to/ha-config
```

For example (when HA config is mounted via Samba):

```bash
./generate_all.py /Volumes/config
```

Then **restart Home Assistant** to apply changes.

## Workflow

1. Edit `rooms.yaml`
2. Run `generate_all.py`
3. Restart Home Assistant
4. The new entities appear automatically

No room lists are duplicated anywhere else.

## HomeKit integration

This system intentionally keeps logic in HA and exposes only:

- `binary_sensor.any_room_needs_heat`

HomeKit automations become simple:

- When the sensor turns **on** → enable heat
- When it turns **off** → disable or lower heat

`heat_permitted` is already baked into the sensor expression.

## Why this exists

- Avoid hand-editing HA helper entities  
- Keep room definitions declarative  
- Support virtual “rooms” like **Away** and **Sleep**  
- Make heating logic deterministic and auditable  
- Work around HomeKit’s limited automation rules

## Future ideas

- Per-room metadata (sleep-mode preference, priorities, etc.)
- Multiple derived sensors (sleep-only, day-mode, etc.)
- Optional validation / `--check` mode in generators


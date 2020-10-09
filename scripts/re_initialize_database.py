#!/usr/bin/env python
# ----------------------------------------------------------------- #
#  File   : re_initialize_database.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.app
import tsl.constants
import tsl.dao.peripheral
import tsl.dao.preset
import tsl.database.sqlite
import tsl.model
import tsl.util.env
import tsl.util.log


import sqlite3


def setup_database(handle):
    handle.executescript("""

CREATE TABLE peripherals (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,
    uuid         TEXT NOT NULL UNIQUE,
    type         TEXT NOT NULL,
    state        TEXT NOT NULL,
    created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE schedules (
    id               INTEGER PRIMARY KEY,
    name             TEXT NOT NULL UNIQUE,
    is_enabled       INTEGER NOT NULL,
    created_at       TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE schedule_items (
    id           INTEGER PRIMARY KEY,
    schedule_id  INTEGER NOT NULL,
    trigger      TEXT NOT NULL,
    preset_id    INTEGER NOT NULL,
    created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (schedule_id) REFERENCES schedules(id),
    FOREIGN KEY (preset_id) REFERENCES presets(id)
);

CREATE TABLE presets (
    id           INTEGER PRIMARY KEY,
    name         INTEGER NOT NULL,
    is_public    INTEGER NOT NULL,
    created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE preset_items (
    id             INTEGER PRIMARY KEY,
    preset_id      INTEGER NOT NULL,
    peripheral_id  INTEGER NOT NULL,
    state          TEXT NOT NULL,
    created_at     TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (preset_id)     REFERENCES presets(id),
    FOREIGN KEY (peripheral_id) REFERENCES peripherals(id)
);

CREATE TABLE nested_presets (
    id               INTEGER PRIMARY KEY,
    preset_id        INTEGER NOT NULL,
    nested_preset_id INTEGER NOT NULL,
    created_at       TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (preset_id)        REFERENCES presets(id),
    FOREIGN KEY (nested_preset_id) REFERENCES presets(id)
);

-- SQLite Doesn't enforce foreign keys by default so fix that.
PRAGMA foreign_keys = ON;

""")


def _associate_preset(parent_id, child_id):
    tsl.dao.preset.associate_nested_preset(parent_id, child_id)


def _build_preset_item(peripheral_id, **state_kwargs):
    return tsl.model.PresetItem(None, peripheral_id, tsl.model.State(**state_kwargs))


def _build_schedule_item(preset_id, **schedule_item_kwargs):
    return tsl.model.ScheduleItem(None, tsl.model.Trigger(**schedule_item_kwargs), preset_id)


def _create_peripheral(name, uuid, peripheral_type, state):
    peripheral = tsl.model.Peripheral(None, name, uuid, peripheral_type, state)
    peripheral_id = tsl.dao.peripheral.create_peripheral(peripheral)
    return peripheral_id


def _create_onoff_peripheral(name, uuid, enabled):
    return _create_peripheral(name, uuid, tsl.constants.PERIPHERAL_TYPE_ONOFF, tsl.model.State(enabled=enabled))


def _create_slider_peripheral(name, uuid, level):
    return _create_peripheral(name, uuid, tsl.constants.PERIPHERAL_TYPE_SLIDER, tsl.model.State(level=level))


def _create_rgb_peripheral(name, uuid, r, g, b):
    return _create_peripheral(name, uuid, tsl.constants.PERIPHERAL_TYPE_RGB, tsl.model.State(r=r, g=g, b=b))


def _create_preset(name, is_public, preset_items):
    preset = tsl.model.Preset(None, name, is_public, preset_items, [])
    preset_id = tsl.dao.preset.create_preset(preset)
    return preset_id


def _create_schedule(name, is_enabled, schedule_items):
    schedule = tsl.model.Schedule(None, name, is_enabled, schedule_items)
    schedule_id = tsl.dao.schedule.create_schedule(schedule)
    return schedule_id


def seed_data(handle):

    tsl.util.log.info('Seeding Peripherals')

    class peripheral:
        grow_lights   = _create_onoff_peripheral('COTS Grow Lights', 'e2cdbfcc-02cf-4a19-aa81-8c000a2f8640', False)  # noqa
        office_left   = _create_rgb_peripheral('Office Left',        'b69eee14-bb98-4236-84eb-45644479430d', r=0, g=0, b=0)  # noqa
        office_center = _create_rgb_peripheral('Office Center',      '745b09f8-49e7-407b-b0d4-d70a248f9f2b', r=0, g=0, b=0)  # noqa
        bedroom       = _create_rgb_peripheral('Bedroom',            '6fa939de-3775-4159-85e4-bd2e4d38ffa2', r=0, g=0, b=0)  # noqa
        hallway       = _create_rgb_peripheral('Hallway',            '516fab6b-6db0-4c68-a1f6-2fbf76f05920', r=0, g=0, b=0)  # noqa
        kitchen       = _create_rgb_peripheral('Kitchen',            '9bbf883b-db13-4aca-ab08-16f71a769084', r=0, g=0, b=0)  # noqa
        tensegrity    = _create_rgb_peripheral('Tensegrity',         '5eef849c-3533-4513-bfa0-a3010bf06858', r=0, g=0, b=0)  # noqa
        crpd1         = _create_rgb_peripheral('CRPD 1',             '296e9040-b70a-4661-ab2c-e024d77aa35b', r=0, g=0, b=0)  # noqa
        crpd2         = _create_rgb_peripheral('CRPD 2',             '022f9ea3-9d67-4e41-ac16-815f6883b910', r=0, g=0, b=0)  # noqa
        crpd3         = _create_rgb_peripheral('CRPD 3',             '85c87440-1b80-42e5-8416-aa902791930a', r=0, g=0, b=0)  # noqa
        crpd4         = _create_rgb_peripheral('CRPD 4',             'da5e1db6-def8-4f7d-aa2d-803ac0e13753', r=0, g=0, b=0)  # noqa

    tsl.util.log.info('Adding Presets')

    class preset:
        everything_on       = _create_preset('Turn Everything On',  True,  [])
        everything_off      = _create_preset('Turn Everything Off', True,  [])
        grow_lights_on      = _create_preset('Grow Lights On',      True,  [_build_preset_item(peripheral.grow_lights, enabled=True)])
        grow_lights_off     = _create_preset('Grow Lights Off',     True,  [_build_preset_item(peripheral.grow_lights, enabled=False)])
        bedroom_morning_on  = _create_preset('_bedroom on',         False, [_build_preset_item(peripheral.bedroom, r=0, g=128, b=255)])
        bedroom_morning_off = _create_preset('_bedroom off',        False, [_build_preset_item(peripheral.bedroom, r=0, g=0, b=0)])

        led_evening = _create_preset('LEDs On', True, [_build_preset_item(peripheral.office_left,   r=0,  g=255,b=0  ),
                                                       _build_preset_item(peripheral.office_center, r=0,  g=0,  b=255),
                                                       _build_preset_item(peripheral.bedroom,       r=128,g=5,  b=255),
                                                       _build_preset_item(peripheral.hallway,       r=128,g=5,  b=255),
                                                       _build_preset_item(peripheral.kitchen,       r=128,g=5,  b=255) ])

        led_night = _create_preset('LEDs Night', True, [_build_preset_item(peripheral.office_left,   r=255,g=30,b=0),
                                                        _build_preset_item(peripheral.office_center, r=255,g=30,b=0),
                                                        _build_preset_item(peripheral.bedroom,       r=255,g=30,b=0),
                                                        _build_preset_item(peripheral.hallway,       r=255,g=30,b=0),
                                                        _build_preset_item(peripheral.kitchen,       r=255,g=30,b=0) ])

        led_off = _create_preset('LEDs Off', True, [_build_preset_item(peripheral.office_left,   r=0, g=0, b=0),
                                                    _build_preset_item(peripheral.office_center, r=0, g=0, b=0),
                                                    _build_preset_item(peripheral.bedroom,       r=0, g=0, b=0),
                                                    _build_preset_item(peripheral.hallway,       r=0, g=0, b=0),
                                                    _build_preset_item(peripheral.kitchen,       r=0, g=0, b=0) ])

        led_white = _create_preset('LEDs White', True, [_build_preset_item(peripheral.office_left, r=255, g=255, b=255),
                                                    _build_preset_item(peripheral.office_center,   r=255, g=255, b=255),
                                                    _build_preset_item(peripheral.bedroom,         r=255, g=255, b=255),
                                                    _build_preset_item(peripheral.hallway,         r=255, g=255, b=255),
                                                    _build_preset_item(peripheral.kitchen,         r=255, g=255, b=255)])

        led_cyberpunk = _create_preset('Cyberpunk', True, [_build_preset_item(peripheral.office_left,   r=255, g=0, b=30 ),
                                                           _build_preset_item(peripheral.office_center, r=0,   g=0, b=255),
                                                           _build_preset_item(peripheral.bedroom,       r=0,   g=0, b=255),
                                                           _build_preset_item(peripheral.hallway,       r=255, g=0, b=30 ),
                                                           _build_preset_item(peripheral.kitchen,       r=0,   g=0, b=255)])

        pixel_day = _create_preset('Pixel Day', True, [ _build_preset_item(peripheral.tensegrity, r=255, g=255, b=255),
                                                        _build_preset_item(peripheral.crpd1,      r=255, g=255, b=255),
                                                        _build_preset_item(peripheral.crpd2,      r=255, g=255, b=255),
                                                        _build_preset_item(peripheral.crpd3,      r=255, g=255, b=255),
                                                        _build_preset_item(peripheral.crpd4,      r=255, g=255, b=255)])

        pixel_night = _create_preset('Pixel Night', True, [ _build_preset_item(peripheral.tensegrity, r=255, g=72, b=3),
                                                            _build_preset_item(peripheral.crpd1,      r=255, g=66, b=6),
                                                            _build_preset_item(peripheral.crpd2,      r=255, g=68, b=10),
                                                            _build_preset_item(peripheral.crpd3,      r=255, g=69, b=10),
                                                            _build_preset_item(peripheral.crpd4,      r=255, g=49, b=7)])

        pixel_cyber_pink = _create_preset('Pixel Cyber Pink', True, [ _build_preset_item(peripheral.tensegrity, r=255, g=0,  b=36),
                                                                      _build_preset_item(peripheral.crpd1,      r=11,  g=0,  b=255),
                                                                      _build_preset_item(peripheral.crpd2,      r=8,   g=0,  b=255),
                                                                      _build_preset_item(peripheral.crpd3,      r=30,  g=13, b=255),
                                                                      _build_preset_item(peripheral.crpd4,      r=18,  g=6,  b=255)])

        pixel_cyber_blue = _create_preset('Pixel Cyber Blue', True, [ _build_preset_item(peripheral.tensegrity, r=0,   g=0, b=255),
                                                                      _build_preset_item(peripheral.crpd1,      r=255, g=3, b=105),
                                                                      _build_preset_item(peripheral.crpd2,      r=255, g=2, b=108),
                                                                      _build_preset_item(peripheral.crpd3,      r=255, g=5, b=101),
                                                                      _build_preset_item(peripheral.crpd4,      r=255, g=2, b=103)])

        pixel_off = _create_preset('Pixel Off', True, [ _build_preset_item(peripheral.tensegrity, r=0,g=0,b=0),
                                                        _build_preset_item(peripheral.crpd1, r=0,g=0,b=0),
                                                        _build_preset_item(peripheral.crpd2, r=0,g=0,b=0),
                                                        _build_preset_item(peripheral.crpd3, r=0,g=0,b=0),
                                                        _build_preset_item(peripheral.crpd4, r=0,g=0,b=0)])
    # If I click _______________ then please also do ___________
    _associate_preset(preset.everything_on, preset.grow_lights_on)
    _associate_preset(preset.everything_on, preset.led_evening)

    _associate_preset(preset.led_evening, preset.pixel_day)
    _associate_preset(preset.led_night, preset.pixel_night)
    _associate_preset(preset.led_white, preset.pixel_day)
    _associate_preset(preset.led_cyberpunk, preset.pixel_cyber_pink)

    _associate_preset(preset.everything_off, preset.grow_lights_off)
    _associate_preset(preset.everything_off, preset.led_off)
    _associate_preset(preset.everything_off, preset.pixel_off)

    _create_schedule('Grow Lights', True, [
        _build_schedule_item(preset.grow_lights_on, hour=6, minute=0),
        _build_schedule_item(preset.grow_lights_off, hour=0, minute=0),
    ])

    _create_schedule('Morning Wake Up', True, [
        _build_schedule_item(preset.bedroom_morning_on, hour=6, minute=0),
        _build_schedule_item(preset.bedroom_morning_off, hour=9, minute=0),
    ])

    _create_schedule('Ambient Lights', True, [
        _build_schedule_item(preset.pixel_day, hour=12, minute=0),
        _build_schedule_item(preset.led_evening, hour=18, minute=0),
        _build_schedule_item(preset.led_night, hour=0, minute=0),
        _build_schedule_item(preset.led_off, hour=1, minute=0),
        _build_schedule_item(preset.pixel_off, hour=1, minute=0),
    ])


def run():
    tsl.util.log.info('Re-Initializing Database')

    database_location = tsl.database.sqlite.get_db_file_location()

    if tsl.util.path.exists_file(database_location):
        tsl.util.log.info('Deleting existing database.')
        tsl.util.path.delete(database_location)

    # Recreate database file.
    tsl.util.log.info('Creating New Database')
    containing_folder = tsl.util.path.get_parent_directory(database_location)
    tsl.util.path.make_directory(containing_folder)
    handle = tsl.database.sqlite.get_database_connection()

    # Get cursor and set up the schema.
    tsl.util.log.info('Populating Tables')
    setup_database(handle)
    tsl.database.sqlite.write_and_close_connection(handle)

    seed_data(handle)

if __name__ == "__main__":
    doc_string = """

Re-Initialize Database

Blows away the existing database and creates a new one with all the default data set up.

Usage:
  re_initialize_database.py
  re_initialize_database.py (-h | --help)

Options:
  -h --help     Show this screen.
  """

    tsl.util.env.get_command_line_args(doc_string)
    tsl.app.initialize()
    run()
    tsl.app.clean_up()

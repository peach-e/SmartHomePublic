#!/usr/bin/env python
# ----------------------------------------------------------------- #
#  File   : re_initialize_database.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.app
import tsl.database.sqlite
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
    mode         TEXT NOT NULL DEFAULT 'FIXED',
    schedule_id  INTEGER DEFAULT NULL,
    created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (schedule_id) REFERENCES schedules(id)
);

CREATE TABLE schedules (
    id               INTEGER PRIMARY KEY,
    name             TEXT NOT NULL UNIQUE,
    peripheral_type  TEXT NOT NULL,
    created_at       TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE schedule_items (
    id           INTEGER PRIMARY KEY,
    schedule_id  INTEGER NOT NULL,
    trigger      TEXT NOT NULL,
    state        TEXT NOT NULL,
    created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (schedule_id) REFERENCES schedules(id)
);

CREATE TABLE presets (
    id           INTEGER PRIMARY KEY,
    name         INTEGER NOT NULL,
    created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE preset_items (
    id             INTEGER PRIMARY KEY,
    preset_id      INTEGER NOT NULL,
    peripheral_id  INTEGER NOT NULL,
    mode           TEXT NOT NULL,
    schedule_id    INTEGER DEFAULT NULL,
    state          TEXT,
    created_at     TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (preset_id)     REFERENCES presets(id),
    FOREIGN KEY (peripheral_id) REFERENCES peripherals(id),
    FOREIGN KEY (schedule_id)   REFERENCES schedules(id)
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


def seed_data(handle):
    handle.executescript("""

-- We don't know how to add peripherals and schedules yet, so we have to do it by hand.
INSERT INTO schedules (id, name, peripheral_type) VALUES
    (1, 'Plant Sunshine',     'ONOFF'),
    (2, 'LED Grow Lights',    'RGB'  ),
    (3, 'Breeze Fans',        'ONOFF'),
    (4, 'Ambient LEDs',       'SLIDER'),
    (5, 'Bedroom Atmosphere', 'RGB'),
    (6, 'Hallway Atmosphere', 'RGB'),
    (7, 'Tensegrity',         'RGB');

INSERT INTO schedule_items (schedule_id, trigger, state) VALUES
    ( 1, '{"hour": 6}',                '{"enabled":true}' ),       -- COTS lights on at 6AM and turn off at 12PM.
    ( 1, '{"hour": 0}',                '{"enabled":false}'),

    ( 2, '{"hour": 7}',                '{"r":0,  "g":255,"b":0}'),   -- LED lights on at 7AM
    ( 2, '{"hour": 0}',                '{"r":255,"g":30, "b":0}'),   -- Turn yellow at midnight
    ( 2, '{"hour": 1}',                '{"r":0,  "g":0,  "b":0}'),   -- Off at 1AM.

    ( 3, '{"minute":0 , "second":0 }', '{"enabled":true}' ),       -- Fans turn on every 0,5,10,15,20,25,...60 and off 30 seconds later.
    ( 3, '{"minute":0 , "second":30}', '{"enabled":false}'),
    ( 3, '{"minute":5 , "second":0 }', '{"enabled":true}' ),
    ( 3, '{"minute":5 , "second":30}', '{"enabled":false}'),
    ( 3, '{"minute":10, "second":0 }', '{"enabled":true}' ),
    ( 3, '{"minute":10, "second":30}', '{"enabled":false}'),
    ( 3, '{"minute":15, "second":0 }', '{"enabled":true}' ),
    ( 3, '{"minute":15, "second":30}', '{"enabled":false}'),
    ( 3, '{"minute":20, "second":0 }', '{"enabled":true}' ),
    ( 3, '{"minute":20, "second":30}', '{"enabled":false}'),
    ( 3, '{"minute":25, "second":0 }', '{"enabled":true}' ),
    ( 3, '{"minute":25, "second":30}', '{"enabled":false}'),
    ( 3, '{"minute":30, "second":0 }', '{"enabled":true}' ),
    ( 3, '{"minute":30, "second":30}', '{"enabled":false}'),
    ( 3, '{"minute":35, "second":0 }', '{"enabled":true}' ),
    ( 3, '{"minute":35, "second":30}', '{"enabled":false}'),
    ( 3, '{"minute":40, "second":0 }', '{"enabled":true}' ),
    ( 3, '{"minute":40, "second":30}', '{"enabled":false}'),
    ( 3, '{"minute":45, "second":0 }', '{"enabled":true}' ),
    ( 3, '{"minute":45, "second":30}', '{"enabled":false}'),
    ( 3, '{"minute":50, "second":0 }', '{"enabled":true}' ),
    ( 3, '{"minute":50, "second":30}', '{"enabled":false}'),
    ( 3, '{"minute":55, "second":0 }', '{"enabled":true}' ),
    ( 3, '{"minute":55, "second":30}', '{"enabled":false}'),

    ( 4, '{"hour": 18}',               '{"level":255}'),             -- Ambient Lights turn on at 6:00PM and off at 1:00AM
    ( 4, '{"hour": 1}',                '{"level":0}'),

    ( 5, '{"hour": 6}',                '{"r":0,  "g":255,"b":255}'), -- Bedroom LED strip turns Blueish at 6AM
    ( 5, '{"hour": 9}',                '{"r":0,  "g":0,  "b":0}'  ), -- ... and off at 9AM
    ( 5, '{"hour": 18}',               '{"r":68, "g":255,"b":190}'), -- ... on again, to greenish teal, at 6PM
    ( 5, '{"hour": 0}',                '{"r":255,"g":30, "b":0}'  ), -- ... change to orange at midnight
    ( 5, '{"hour": 1}',                '{"r":0,  "g":0,  "b":0}'  ), -- ... and off at 1AM.

    ( 6, '{"hour": 18}',               '{"r":128, "g":30, "b":255}'), -- ... Hallway turns blueish purple at 6PM.
    ( 6, '{"hour": 0}',                '{"r":255, "g":30, "b":0}'  ), -- ... change to orange at midnight
    ( 6, '{"hour": 1}',                '{"r":0,   "g":0,  "b":0}'  ), -- ... and off at 1AM.

    ( 7, '{"hour": 12}',               '{"r":255, "g":255, "b":255}'), -- Tensegrity goes white at noon.
    ( 7, '{"hour": 0}',                '{"r":255, "g":30,  "b":0}'  ), -- Orange at midnight.
    ( 7, '{"hour": 1}',                '{"r":0,   "g":0,   "b":0}'  ); -- Off at 1AM.

INSERT INTO peripherals (id, name, uuid, type, state, mode, schedule_id) VALUES
    (1,  'COTS Grow Lights', 'e2cdbfcc-02cf-4a19-aa81-8c000a2f8640', 'ONOFF',  '{"enabled":false}',       'SCHEDULED', 1),
    (2,  'LED Grow Lights',  'b3c23f37-b7ae-45ec-9a7c-c162e061a826', 'RGB',    '{"r":0,"g":0,"b":0}',     'SCHEDULED', 2),
    (3,  'Breeze Fans',      '6826ed06-c7d0-4538-97b8-491891fcc134', 'ONOFF',  '{"enabled":false}',       'SCHEDULED', 3),
    (4,  'Blue Ambient',     '34166325-2d5c-49bf-a89a-c36f991c07bd', 'SLIDER', '{"level":0}',             'SCHEDULED', 4),
    (5,  'Green Ambient',    '8c639c8c-7c45-41cc-bb86-b11d0a98e90e', 'SLIDER', '{"level":0}',             'SCHEDULED', 4),
    (6,  'RGB Bedroom',      '6fa939de-3775-4159-85e4-bd2e4d38ffa2', 'RGB',    '{"r":0,"g":0,"b":0}',     'SCHEDULED', 5),
    (7,  'RGB Hallway',      '516fab6b-6db0-4c68-a1f6-2fbf76f05920', 'RGB',    '{"r":0,"g":0,"b":0}',     'SCHEDULED', 6),
    (8,  'Tensegrity',       '5eef849c-3533-4513-bfa0-a3010bf06858', 'RGB',    '{"r":0,"g":0,"b":0}',     'SCHEDULED', 7),
    (9,  'CRPD 1',           '296e9040-b70a-4661-ab2c-e024d77aa35b', 'RGB',    '{"r":255,"g":0,"b":0}',   'FIXED', NULL),
    (10, 'CRPD 2',           '022f9ea3-9d67-4e41-ac16-815f6883b910', 'RGB',    '{"r":0,"g":255,"b":0}',   'FIXED', NULL),
    (11, 'CRPD 3',           '85c87440-1b80-42e5-8416-aa902791930a', 'RGB',    '{"r":0,"g":0,"b":255}',   'FIXED', NULL),
    (12, 'CRPD 4',           'da5e1db6-def8-4f7d-aa2d-803ac0e13753', 'RGB',    '{"r":255,"g":0,"b":255}', 'FIXED', NULL);

INSERT INTO presets (id, name) VALUES
    (1, 'Turn Everything On'  ),
    (2, 'Turn Everything Off' ),
    (3, 'Resume Schedules'    ),
    (4, 'LEDs On'             ),
    (5, 'LEDs Off'            ),
    (6, 'LEDs Scheduled'      ),
    (7, 'Pixel Day'           ),
    (8, 'Pixel Night'         ),
    (9, 'Pixel Off'           );

INSERT INTO nested_presets (preset_id, nested_preset_id) VALUES
    (1, 4), -- Preset 1 executes Preset 4 as part of its things to do.
    (2, 5),
    (3, 6),
    (4, 7),
    (5, 9);

INSERT INTO preset_items (preset_id, peripheral_id, mode, schedule_id, state) VALUES
    -- Grow Lights On, Off, Resume Schedules.
    (1, 1, 'FIXED',     NULL, '{"enabled":true}' ),
    (2, 1, 'FIXED',     NULL, '{"enabled":false}'),
    (3, 1, 'SCHEDULED', 1,     NULL              ),

    -- All LEDs On
    (4, 2, 'FIXED', NULL, '{"r":0,"g":255,"b":0}'),
    (4, 4, 'FIXED', NULL, '{"level":255}'),
    (4, 5, 'FIXED', NULL, '{"level":255}'),
    (4, 6, 'FIXED', NULL, '{"r":68, "g":255,"b":190}'),
    (4, 7, 'FIXED', NULL, '{"r":128,"g":30, "b":255}'),

    -- All LEDs Off
    (5, 2, 'FIXED', NULL, '{"r":0,"g":0,"b":0}'),
    (5, 4, 'FIXED', NULL, '{"level":0}'),
    (5, 5, 'FIXED', NULL, '{"level":0}'),
    (5, 6, 'FIXED', NULL, '{"r":0,"g":0,"b":0}'),
    (5, 7, 'FIXED', NULL, '{"r":0,"g":0,"b":0}'),
    (5, 8, 'FIXED', NULL, '{"r":0,"g":0,"b":0}'),

    -- All LEDs resume schedules.
    (6, 2, 'SCHEDULED', 2, NULL),
    (6, 4, 'SCHEDULED', 4, NULL), -- For preset 6, device ID 4 will take on schedule 4.
    (6, 5, 'SCHEDULED', 4, NULL),
    (6, 6, 'SCHEDULED', 5, NULL),
    (6, 7, 'SCHEDULED', 6, NULL),
    (6, 8, 'SCHEDULED', 7, NULL),

    -- Pixel Display Daytime
    (7, 8,  'FIXED', NULL, '{"r":255,"g":255, "b":255}'),
    (7, 9,  'FIXED', NULL, '{"r":12, "g":255, "b":128}'),
    (7, 10, 'FIXED', NULL, '{"r":0,  "g":12,  "b":255}'),
    (7, 11, 'FIXED', NULL, '{"r":0,  "g":255, "b":12 }'),
    (7, 12, 'FIXED', NULL, '{"r":12, "g":128, "b":255}'),

    -- Pixel Display Night
    (8, 8,  'FIXED', NULL, '{"r":255, "g":30,  "b":0  }'),
    (8, 9,  'FIXED', NULL, '{"r":255, "g":128, "b":32 }'),
    (8, 10, 'FIXED', NULL, '{"r":255, "g":64,  "b":0  }'),
    (8, 11, 'FIXED', NULL, '{"r":255, "g":42,  "b":16 }'),
    (8, 12, 'FIXED', NULL, '{"r":255, "g":100, "b":25 }'),

    -- Pixel Display Off
    (9, 9,  'FIXED', NULL, '{"r":0, "g":0, "b":0 }'),
    (9, 10, 'FIXED', NULL, '{"r":0, "g":0, "b":0 }'),
    (9, 11, 'FIXED', NULL, '{"r":0, "g":0, "b":0 }'),
    (9, 12, 'FIXED', NULL, '{"r":0, "g":0, "b":0 }');
""")


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
    seed_data(handle)

    # Commit and Close
    tsl.database.sqlite.write_and_close_connection(handle)

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

# ----------------------------------------------------------------- #
#  File   : helper.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import time

ONE_DAY_SECONDS = 86400


def get_active_schedule_item(schedule_items):
    time_schedule_item = {}
    HMS_now = _get_HMS_now()

    for schedule_item in schedule_items:
        time_since_trigger = _get_time_since_trigger(
            schedule_item.trigger, HMS_now)
        time_schedule_item[time_since_trigger] = schedule_item

    most_recent_key = min(time_schedule_item.keys())
    return time_schedule_item[most_recent_key]


def _get_HMS_now():
    return [int(x) for x in time.strftime("%H %M %S").split(' ')]


def _get_time_since_trigger(trigger, HMS_now):
    # Given a trigger object, and a array of [23, 59, 59] timestamp,
    # calculate the most recent number of seconds where there was
    # a match.

    hours = []
    minutes = []
    seconds = []

    if trigger.hour is None:
        h = HMS_now[0]
        hours = [h, _saain(h, 24)]
    else:
        hours = [trigger.hour]

    if trigger.minute is None:
        m = HMS_now[1]
        minutes = [m, _saain(m, 60)]
    else:
        minutes = [trigger.minute]

    if trigger.second is None:
        s = HMS_now[2]
        seconds = [s, _saain(s, 60)]
    else:
        seconds = [trigger.second]

    elapsed_times = []
    for h in hours:
        for m in minutes:
            for s in seconds:
                elapsed_times.append(_get_time_since([h, m, s], HMS_now))

    return min(elapsed_times)


def _get_time_since(HMS, HMS_now):
    seconds = 3600 * HMS[0] + 60 * HMS[1] + HMS[2]
    seconds_now = 3600 * HMS_now[0] + 60 * HMS_now[1] + HMS_now[2]

    delta_t = seconds_now - seconds
    if delta_t < 0:
        delta_t += ONE_DAY_SECONDS

    return delta_t


def _saain(value, number_to_add):
    # "Subtract And Add If Negative"
    result = value - 1
    if result < 0:
        result += number_to_add
    return result

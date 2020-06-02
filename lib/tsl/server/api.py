# ----------------------------------------------------------------- #
#  File   : api.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.services
import tsl.util.exception
import tsl.util.log
import json

_MESSAGE_404 = 'Unknown Endpoint'
_MIME_TYPE_JSON = "application/json"
_MIME_TYPE_TEXT = "text/html"

_RESULT_200 = 200
_RESULT_400 = 400
_RESULT_404 = 404

_METHOD_TYPE_GET = 'GET'
_METHOD_TYPE_POST = 'POST'


class APIResult:

    def __init__(self, status, mimetype, data):
        self.status = status
        self.mimetype = mimetype
        self.data = data

        if type(data) is not str:
            raise tsl.util.exception.DataError('API result must be a string.')


def _create_400_result(message):
    return APIResult(_RESULT_400, _MIME_TYPE_TEXT, message)


def _create_404_result():
    return APIResult(_RESULT_404, _MIME_TYPE_TEXT, _MESSAGE_404)


def _create_data_result(data_structure):
    data_json = json.dumps(data_structure)
    return APIResult(_RESULT_200, _MIME_TYPE_JSON, data_json)


def handle_request(method, endpoint, data):

    #
    # Requests are handled by forming a function name out of the end point and seeing if we have one here.
    # Convert something like GET /api/devices/help/" to get_devices_help.
    #
    function_name = method.lower() + \
        endpoint[4:].rstrip('/').replace('/', '_')

    if _API_FUNCTIONS.get(function_name) is None:
        tsl.util.log.warn('Unknown API function {}.'.format(function_name))
        return _create_404_result()

    return _API_FUNCTIONS[function_name](data)

# ------------------------------------------------- #
#                 API FUNCTIONS                     #
# ------------------------------------------------- #

#
# Peripherals
#


def get_peripherals(data):
    result_data = []
    for peripheral in tsl.services.get_peripherals():
        result_data.append(peripheral.convert_to_dictionary())
    return _create_data_result(result_data)


def post_peripheral_schedule(data):
    result_data = []
    peripheral_id = data['peripheral_id']
    schedule_id = data['schedule_id']

    sc = tsl.services.set_peripheral_schedule(peripheral_id, schedule_id)

    if sc:
        return _create_data_result({})
    else:
        return _create_400_result('Cannae update peripheral {} with schedule {}.'.format(peripheral_id, schedule_id))


def post_peripheral_state(data):
    peripheral_id = data['peripheral_id']
    state = data['state']

    sc = tsl.services.set_peripheral_state(peripheral_id, state)

    if sc:
        return _create_data_result({})
    else:
        return _create_400_result('Cannae update peripheral {} with value {}.'.format(peripheral_id, state))

#
# Presets
#


def get_presets(data):
    result_data = []
    for preset in tsl.services.get_presets():
        result_data.append(preset.convert_to_dictionary())
    return _create_data_result(result_data)


def post_preset(data):
    preset_id = data['preset_id']

    sc = tsl.services.apply_preset(preset_id)
    if sc:
        return _create_data_result({})
    else:
        return _create_400_result('Failed to apply preset {}.'.format(preset_id))

#
# Schedules
#


def get_schedules(data):
    result_data = []
    for schedule in tsl.services.get_schedules():
        result_data.append(schedule.convert_to_dictionary())
    return _create_data_result(result_data)


_API_FUNCTIONS = {
    'get_peripherals': get_peripherals,
    'post_peripheral_schedule': post_peripheral_schedule,
    'post_peripheral_state': post_peripheral_state,
    'post_preset': post_preset,
    'get_presets': get_presets,
    'get_schedules': get_schedules,
}

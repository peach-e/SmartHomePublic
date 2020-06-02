# ----------------------------------------------------------------- #
#  File   : http.py
#  Author : peach
#  Date   : 24 May 2020
# ----------------------------------------------------------------- #

import tsl.configuration
import tsl.constants
import tsl.rgb
import tsl.util.path

from urllib import request, parse
import json

USE_MOCK = tsl.configuration.val('USE_MOCK_HTTP')
if USE_MOCK:
    tsl.util.log.warn('MOCK - Using mock HTTP')


def _get_http_endpoint(pixel):
    ip = tsl.configuration.val('HTTP_CRPD_IP_ADDRESS')
    route = tsl.constants.HTTP_CRPD_ROUTE
    endpoint = tsl.util.path.join_paths('http://', ip, route, str(pixel))
    return endpoint


def set_crpd_pixel(pixel, r, g, b):
    try:
        assert type(pixel) is int
        assert tsl.rgb.is_rgb_valid(r, g, b)
    except AssertionError:
        tsl.util.log.error('Error setting RGB level to CRPD Pixel.')
        return 0

    url = _get_http_endpoint(pixel)
    data = json.dumps({"r": r, "g": g, "b": b}).encode()

    if USE_MOCK:
        tsl.util.log.warn(f'MOCK - Setting CRPD Pixel {pixel} to {r}, {g}, {b}.')
        return

    req = request.Request(url, data=data)
    request.urlopen(req)

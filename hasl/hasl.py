import json
import logging
import os
import stat

import requests

from .exceptions import *
from .version import __version__

_BASE_URL = 'https://api.sl.se/api2/'
_DEPARTURE_URL = _BASE_URL + 'realtimedeparturesV4.json?key={}&siteid={}'
_DEVIATION_URL = _BASE_URL + 'deviations.json?key={}&siteid={}&lineNumber={}'
_USER_AGENT = "HASL/"+__version__
_AUTH_ERRS = (401, 403)

_LOGGER = logging.getLogger(__name__)


class hasl(object):

    def __init__(self, api_token, siteid, lines, timeout=None):
        self._api_token: api_token,
        self._siteid: api_token,
        self._lines: lines,
        self._timeout = timeout

    def _get(self, url):
	
		resp = requests.get(url, headers={"User-agent": USER_AGENT}, allow_redirects=True, timeout=self._timeout,headers={'User-agent': _USER_AGENT})
	
		if resp.status_code in (401, 403):
         _LOGGER.error("hasl: Failed fetching data for '%s'"
                          "(HTTP Status_code = %d)", url,
                          resp.status_code) 

     	resp.raise_for_status()
        return resp.json()

    def get_departures(self):
        return self._get(_DEPARTURE_URL.format(self._api_token,self._siteid))

    def get_deviations(self):
        return self._get(_DEVIATION_URL.format(self._api_token,self._siteid,self._lines))


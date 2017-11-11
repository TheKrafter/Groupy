import logging

import requests

from . import exceptions


logger = logging.getLogger(__name__)


class Session(requests.Session):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.headers = {'content-type': 'application/json'}

    def request(self, *args, **kwargs):
        # inject the access token
        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params']['token'] = self.token

        # ensure we reraise exceptions as our own
        try:
            response = super().request(*args, **kwargs)
            response.raise_for_status()
            return Response(response)
        except requests.HTTPError as e:
            logger.exception('received a bad response')
            raise exceptions.BadResponse(response) from e
        except requests.RequestException as e:
            logger.exception('could not receive a response')
            raise exceptions.NoResponse(e.request) from e


class Response:
    def __init__(self, response):
        self._resp = response

    # pretend we're a requests.Response
    def __getattr__(self, attr):
        return getattr(self._resp, attr)

    @property
    def data(self):
        try:
            return self.json()['response']
        except ValueError as e:
            raise exceptions.InvalidJsonError(self._resp) from e
        except KeyError as e:
            raise exceptions.MissingResponseError(self._resp) from e

    @property
    def errors(self):
        try:
            return self.json()['meta']['errors']
        except ValueError as e:
            raise exceptions.InvalidJsonError(self._resp) from e
        except KeyError as e:
            raise exceptions.MissingMetaError(self._resp) from e

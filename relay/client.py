import io
import json

import requests

from . import exceptions

__all__ = ['Client']


class Client:
    """
    A client for the Relay API.
    """

    def __init__(
        self,
        api_key,
        api_base_url='https://api.relay.ninja',
        timeout=None,
        encoder=None
    ):

        # A key used to authenticate API calls to an account
        self._api_key = api_key

        # The base URL to use when calling the API
        self._api_base_url = api_base_url

        # The period of time before requests to the API should timeout
        self._timeout = timeout

        # The encoder used to serialize messages that are not passed as strings
        self._encoder = encoder or json.dumps

        # NOTE: Rate limiting information is only available after a request
        # has been made.

        # The maximum number of requests per second that can be made with the
        # given API key.
        self._rate_limit = None

        # The time (seconds since epoch) when the current rate limit will
        # reset.
        self._rate_limit_reset = None

        # The number of requests remaining within the current limit before the
        # next reset.
        self._rate_limit_remaining = None

    @property
    def rate_limit(self):
        return self._rate_limit

    @property
    def rate_limit_reset(self):
        return self._rate_limit_reset

    @property
    def rate_limit_remaining(self):
        return self._rate_limit_remaining

    def __call__(self,
        method,
        path,
        params=None,
        data=None
    ):
        """Call the API"""

        # Build headers
        headers = {
            'Accept': 'application/json',
            'X-Relay-APIKey': self._api_key
        }

        if params:
            # Filter out parameters set to `None`
            params = {k: v for k, v in params.items() if v is not None}

        if data:
            # Filter out data set to `None`
            data = {k: v for k, v in data.items() if v is not None}

        # Make the request
        r = getattr(requests, method.lower())(
            f'{self._api_base_url}/{path}',
            headers=headers,
            params=params,
            data=data,
            timeout=self._timeout
        )

        # Update the rate limit
        if 'X-Relay-RateLimit-Limit' in r.headers:
            self._rate_limit = int(r.headers['X-Relay-RateLimit-Limit'])
            self._rate_limit_reset = float(r.headers['X-Relay-RateLimit-Reset'])
            self._rate_limit_remaining \
                    = int(r.headers['X-Relay-RateLimit-Remaining'])

        # Handle a successful response
        if r.status_code in [200, 204]:
            return None

        # Raise an error related to the response
        try:
            error = r.json()

        except ValueError:
            error = {}

        error_cls = exceptions.RelayException.get_class_by_status_code(
            r.status_code
        )

        raise error_cls(
            r.status_code,
            error.get('hint'),
            error.get('arg_errors')
        )

    def encode(self, v):
        return self._encoder(v)

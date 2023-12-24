# -*- coding: utf-8 -*-
import json
from copy import copy
from types import ModuleType
from typing import Any

import requests

from omdb.config import config
from omdb.exceptions.base import OmdbRequestException
from omdb.log import log


class OmdbRequest:
    request_supported_methods: list[str] = ['GET']
    request_base_url: str = 'https://www.omdbapi.com/'
    request_headers: dict[str, str] = {}
    request_params: dict[str, Any] = {'apikey': config.OMDB_API_KEY, 'type': config.OMDB_DATA_TYPE}
    request_log_response_codes: list[int] = [500, 403]
    request_session: bool = True
    request_json: bool = True

    def __init__(
        # pylint: disable=too-many-arguments
        self,
        supported_methods: list[str] = None,
        base_url: str = None,
        headers: dict[str, str] = None,
        log_response_codes: list[int] = None,
        session: bool = None,
        request_json: bool = None,
    ):
        if supported_methods:
            self.request_supported_methods = supported_methods

        if base_url:
            self.request_base_url = base_url

        if headers:
            self.request_headers.update(headers)

        if log_response_codes:
            self.request_log_response_codes = log_response_codes

        # Override settings
        if session is not None:
            self.request_session = session

        if request_json is not None:
            self.request_json = request_json

        self.session: ModuleType | requests.Session = requests
        if self.request_session:
            self.session = requests.Session()

    def _request(
        self,
        method: str,
        url_path: str = '',
        data: Any = None,
        params: dict[str, Any] = None,
        **kwargs: dict,
    ) -> dict:
        if method not in self.request_supported_methods:
            raise OmdbRequestException(f'Methods allowed: {self.request_supported_methods}')

        method = method.lower()
        url = f'{self.request_base_url}{url_path}'

        if data and self.request_json:
            data = json.dumps(data)

        request_params = copy(self.request_params)
        if params:
            request_params.update(params)

        headers = copy(self.request_headers)
        headers.update(kwargs.get('headers', {}))
        kwargs['headers'] = headers
        response: requests.Response = getattr(self.session, method)(url=url, data=data, params=request_params, **kwargs)

        if not response:
            raise OmdbRequestException('Empty response')

        # Log response codes in this list, off by default
        if self.request_log_response_codes and response.status_code in self.request_log_response_codes:
            log.error(
                'CORE - OMDB request returned %s with the text %s against %s %s, data: %s, params: %s',
                response.status_code,
                response.text,
                method,
                url,
                data,
                params,
            )
            raise OmdbRequestException(f'Request failed: {response.text}')

        return response.json()

    def search(self, page: int = None, **kwargs) -> dict:
        _params: dict[str, Any] = {'s': config.OMDB_SEARCH_KEY}
        if page:
            _params.update({'page': page})
        return self._request(method='GET', params=_params, **kwargs)

    def get_by_imdb_id(self, imdb_id: str, **kwargs) -> dict:
        _params = {'i': imdb_id}
        return self._request(method='GET', params=_params, **kwargs)

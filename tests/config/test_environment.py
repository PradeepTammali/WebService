# -*- coding: utf-8 -*-
from unittest.mock import mock_open, patch

import pytest
from pytest import MonkeyPatch

from omdb.config.environment import get_environment, is_running_in_docker


@pytest.mark.parametrize('environment', ['production', 'development', 'test', 'unittest'])
def test_get_environment(monkeypatch: MonkeyPatch, environment: str):
    monkeypatch.setenv('ENVIRONMENT', environment)
    result = get_environment()
    assert result == environment


def test_get_environment_invalid(monkeypatch: MonkeyPatch):
    monkeypatch.setenv('ENVIRONMENT', 'invalid')
    with pytest.raises(ValueError):
        get_environment()


def test_is_running_in_docker():
    with patch('builtins.open', mock_open(read_data='sample')):
        assert is_running_in_docker() is False

    with patch('builtins.open', mock_open(read_data='docker')):
        assert is_running_in_docker() is True

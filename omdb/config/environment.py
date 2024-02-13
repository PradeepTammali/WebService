# -*- coding: utf-8 -*-
import os

ENABLED_ENVIRONMENTS = [
    'production',
    'development',
    'test',
    'unittest',
]


def get_environment() -> str:
    environment = os.environ.get('ENVIRONMENT', os.environ.get('APP_ENVIRONMENT', 'development'))
    if environment.lower() not in ENABLED_ENVIRONMENTS:
        raise ValueError(f'Invalid environment: {environment}')

    return environment


def is_running_in_docker() -> bool:
    try:
        with open('/proc/1/cgroup', 'r', encoding='utf-8') as fp:
            return 'docker' in fp.read()
    except FileNotFoundError:
        return False

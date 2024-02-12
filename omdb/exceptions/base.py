# -*- coding: utf-8 -*-
class OmdbBaseException(Exception):
    pass


class OmdbQueryException(OmdbBaseException):
    pass


class OmdbQueryMultipleResultsException(OmdbBaseException):
    pass


class OmdbRequestException(OmdbBaseException):
    pass


class OmdbInvalidDataException(OmdbBaseException):
    pass


class OmdbModelNotFoundException(OmdbBaseException):
    pass


class OmdbUserException(OmdbBaseException):
    pass

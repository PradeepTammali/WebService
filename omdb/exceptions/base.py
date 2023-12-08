# -*- coding: utf-8 -*-
class OmdbBaseException(Exception):
    pass


class OmdbQueryException(OmdbBaseException):
    pass


class OmdbQueryMultipleResultsException(OmdbBaseException):
    pass

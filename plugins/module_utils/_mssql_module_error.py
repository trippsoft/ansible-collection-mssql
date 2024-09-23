#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class MssqlModuleError():
    """
    Represents an error that occurred in a Microsoft SQL Server module.
    """

    message: str
    exception: str | None

    def __init__(self, message: str, exception: str | None = None):
        self.message = message
        self.exception = exception

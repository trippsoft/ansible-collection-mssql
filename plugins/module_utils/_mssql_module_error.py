# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from typing import Optional


class MssqlModuleError():
    """
    Represents an error that occurred in a Microsoft SQL Server module.
    """

    message: str
    exception: Optional[str]

    def __init__(self, message: str, exception: Optional[str] = None) -> None:
        self.message = message
        self.exception = exception

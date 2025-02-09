# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)


class ModuleDocFragment(object):

    DOCUMENTATION = r"""
    options:
      login_user:
        type: str
        required: true
        description:
          - The username with which to authenticate to the SQL Server instance.
      login_password:
        type: str
        required: true
        description:
          - The password with which to authenticate to the SQL Server instance.
      login_host:
        type: str
        required: true
        description:
          - The hostname of the SQL Server instance to configure.
      login_port:
        type: int
        required: false
        default: 1433
        description:
          - The port on which the SQL Server instance is listening.
    """

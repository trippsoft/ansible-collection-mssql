# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import traceback

from typing import Optional

from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.basic import AnsibleModule

from ._mssql_module_error import MssqlModuleError

LOGIN_ARGSPEC: dict = dict(
    login_user=dict(type='str', required=True),
    login_password=dict(type='str', required=True, no_log=True),
    login_host=dict(type='str', required=True),
    login_port=dict(type='int', required=False, default=1433)
)

try:
    import pymssql
except ImportError:
    HAS_PYMSSQL: bool = False
    PYMSSQL_IMPORT_ERROR: Optional[str] = traceback.format_exc()

    class MssqlModule(AnsibleModule):

        def __init__(
                self,
                *args,
                argument_spec: Optional[dict] = None,
                **kwargs) -> None:

            if argument_spec is None:
                argument_spec: dict = {}

            argspec: dict = MssqlModule.generate_argspec(**argument_spec)

            super(MssqlModule, self).__init__(
                *args,
                argument_spec=argspec,
                supports_check_mode=True,
                **kwargs
            )

        @classmethod
        def generate_argspec(cls, **kwargs) -> dict:
            """
            Generates an argument specification for a Microsoft SQL Server module.

            Args:
                **kwargs: Additional arguments to include in the specification.

            Returns:
                dict: The argument specification.
            """

            return dict(
                **LOGIN_ARGSPEC,
                **kwargs
            )

else:
    HAS_PYMSSQL: bool = True
    PYMSSQL_IMPORT_ERROR: Optional[str] = None

    class MssqlModule(AnsibleModule):
        """
        Extends AnsibleModule to simplify the creation of Microsoft SQL Server modules.
        """

        conn: pymssql.Connection
        cursor: pymssql.Cursor

        def __init__(
                self,
                *args,
                argument_spec: Optional[dict] = None,
                **kwargs) -> None:

            if argument_spec is None:
                argument_spec: dict = {}

            argspec: dict = MssqlModule.generate_argspec(**argument_spec)

            self.conn = None
            self.cursor = None

            super(MssqlModule, self).__init__(
                *args,
                argument_spec=argspec,
                supports_check_mode=True,
                **kwargs
            )

        @classmethod
        def generate_argspec(cls, **kwargs) -> dict:
            """
            Generates an argument specification for a Microsoft SQL Server module.

            Args:
                **kwargs: Additional arguments to include in the specification.

            Returns:
                dict: The argument specification.
            """

            return dict(
                **LOGIN_ARGSPEC,
                **kwargs
            )

        def close_client_session(self) -> None:
            """
            Closes the Microsoft SQL Server client session.
            """

            if self.cursor is not None:
                self.cursor.close()
                self.cursor = None

            if self.conn is not None:
                self.conn.close()
                self.conn = None

        def handle_error(self, error) -> None:
            """
            Handle an error, if it occurred, in the module.

            Args:
                error (Any): A value that could be a MssqlModuleError.
            """

            if isinstance(error, MssqlModuleError):
                self.close_client_session()
                self.fail_json(msg=error.message, exception=error.exception)

        def initialize_client(self) -> None:
            """
            Initializes the Microsoft SQL Server client.
            If an error occurs, the module failure is handled.
            """

            login_user = self.params['login_user']
            login_password = self.params['login_password']
            login_host = self.params['login_host']
            login_port = self.params['login_port']

            try:
                self.conn = pymssql.connect(
                    server=login_host,
                    port=login_port,
                    user=login_user,
                    password=login_password,
                    as_dict=True
                )
            except pymssql.Error as e:
                self.fail_json(msg=to_native(e))

            self.cursor = self.conn.cursor()

        def get_defined_non_connection_params(self) -> dict:
            """
            Get the defined non-connection parameters for the module.

            Returns:
                dict: The defined non-connection parameters for the module.
            """

            filtered_params: dict = self.params.copy()
            delete_keys: list[str] = [key for key in self.params.keys() if key in LOGIN_ARGSPEC]

            for key in delete_keys:
                del filtered_params[key]

            delete_keys: list[str] = [key for key in self.params.keys() if self.params[key] is None]

            for key in delete_keys:
                del filtered_params[key]

            return filtered_params

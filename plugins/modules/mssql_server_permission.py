#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
module: mssql_server_permission
version_added: 1.0.0
author:
  - Jim Tarpley (@trippsc2)
short_description: Configures a SQL server-level permission in a Microsoft SQL Server instance.
description:
  - Configures a SQL server-level permission in a Microsoft SQL Server instance.
attributes:
  check_mode:
    support: full
    description:
      - This module supports check mode.
extends_documentation_fragment:
  - trippsc2.mssql.login
options:
  principal:
    type: str
    required: true
    description:
      - The name of the SQL login or role for which to configure server-level permissions.
  permissions:
    type: list
    required: true
    elements: str
    choices:
      - administer_bulk_operations
      - alter_any_availability_group
      - alter_any_connection
      - alter_any_credential
      - alter_any_database
      - alter_any_endpoint
      - alter_any_event_notification
      - alter_any_event_session
      - alter_any_linked_server
      - alter_any_login
      - alter_any_server_audit
      - alter_any_server_role
      - alter_resources
      - alter_server_state
      - alter_settings
      - alter_trace
      - authenticate_server
      - connect_any_database
      - connect_sql
      - control_server
      - create_any_database
      - create_availability_group
      - create_ddl_event_notification
      - create_endpoint
      - create_server_role
      - create_trace_event_notification
      - external_access_assembly
      - impersonate_any_login
      - select_all_user_securables
      - shutdown
      - unsafe_assembly
      - view_any_database
      - view_any_definition
      - view_server_state
    description:
      - The type of server-level permission to configure.
  state:
    type: str
    required: false
    default: grant
    choices:
      - grant
      - deny
      - grant_with_grant_option
      - revoke
    description:
      - The state of the server-level permissions.
"""

EXAMPLES = r"""
- name: Grant SQL server-level permissions
  trippsc2.mssql.mssql_server_permission:
    login_user: sa
    login_password: password
    login_host: localhost
    principal: test
    permissions:
      - connect_sql
      - view_server_state
    state: grant

- name: Deny SQL server-level permissions
  trippsc2.mssql.mssql_server_permission:
    login_user: sa
    login_password: password
    login_host: localhost
    principal: test
    permissions:
      - connect_sql
      - view_server_state
    state: deny

- name: Grant SQL server-level permissions with grant option
  trippsc2.mssql.mssql_server_permission:
    login_user: sa
    login_password: password
    login_host: localhost
    principal: test
    permissions:
      - connect_sql
      - view_server_state
    state: grant_with_grant_option

- name: Remove SQL server-level permissions
  trippsc2.mssql.mssql_server_permission:
    login_user: sa
    login_password: password
    login_host: localhost
    principal: test
    permissions:
      - connect_sql
      - view_server_state
    state: revoke
"""

RETURN = r"""
current:
  type: dict
  returned: O(state=present)
  description:
    - The configuration of the SQL server-level permissions.
  sample:
    - permission: connect_sql
      state: grant_with_grant_option
    - permission: view_server_state
      state: grant_with_grant_option
  contains:
    permission:
      type: str
      description:
        - The server-level permission.
    state:
      type: str
      description:
        - The state of the server-level permission.
previous:
  type: dict
  returned: changed
  description:
    - The previous configuration of the SQL server-level permissions.
  sample:
    - permission: connect_sql
      state: grant
    - permission: view_server_state
      state: deny
  contains:
    permission:
      type: str
      description:
        - The server-level permission.
    state:
      type: str
      description:
        - The state of the server-level permission.
"""

import traceback

from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.common.text.converters import to_native

from typing import Optional

try:
    import pymssql
except ImportError:
    HAS_PYMSSQL: bool = False
    PYMSSQL_IMPORT_ERROR: Optional[str] = traceback.format_exc()
else:
    HAS_PYMSSQL: bool = True
    PYMSSQL_IMPORT_ERROR: Optional[str] = None

from ..module_utils._mssql_module import MssqlModule
from ..module_utils._mssql_module_error import MssqlModuleError


def run_module() -> None:
    module: MssqlModule = MssqlModule(
        argument_spec=dict(
            principal=dict(type='str', required=True),
            permissions=dict(
                type='list',
                required=True,
                elements='str',
                choices=[
                    'administer_bulk_operations',
                    'alter_any_availability_group',
                    'alter_any_connection',
                    'alter_any_credential',
                    'alter_any_database',
                    'alter_any_endpoint',
                    'alter_any_event_notification',
                    'alter_any_event_session',
                    'alter_any_linked_server',
                    'alter_any_login',
                    'alter_any_server_audit',
                    'alter_any_server_role',
                    'alter_resources',
                    'alter_server_state',
                    'alter_settings',
                    'alter_trace',
                    'authenticate_server',
                    'connect_any_database',
                    'connect_sql',
                    'control_server',
                    'create_any_database',
                    'create_availability_group',
                    'create_ddl_event_notification',
                    'create_endpoint',
                    'create_server_role',
                    'create_trace_event_notification',
                    'external_access_assembly',
                    'impersonate_any_login',
                    'select_all_user_securables',
                    'shutdown',
                    'unsafe_assembly',
                    'view_any_database',
                    'view_any_definition',
                    'view_server_state'
                ]
            ),
            state=dict(
                type='str',
                required=False,
                default='grant',
                choices=['grant', 'deny', 'grant_with_grant_option', 'revoke']
            )
        )
    )

    if not HAS_PYMSSQL:
        module.fail_json(
            msg=missing_required_lib('pymssql'),
            exception=PYMSSQL_IMPORT_ERROR)

    params: dict = module.get_defined_non_connection_params()
    module.initialize_client()
    validate_params(params, module)

    previous_permissions: dict = get_server_permissions(params['principal'], params['permissions'], module)

    changed: bool = False

    previous: list[dict] = []
    current: list[dict] = []

    for permission, previous_state in previous_permissions.items():
        if previous_state != params['state']:
            changed: bool = True

        if previous_state != 'revoke':
            previous.append(dict(permission=permission, state=previous_state))

        if params['state'] != 'revoke':
            current.append(dict(permission=permission, state=params['state']))

        if not module.check_mode:
            modify_permission(
                params['principal'],
                permission,
                previous_state,
                params['state'],
                module
            )

    if len(previous) > 0:
        if len(current) > 0:
            result: dict = dict(changed=changed, previous=previous, current=current)
        else:
            result: dict = dict(changed=changed, previous=previous)
    else:
        if len(current) > 0:
            result: dict = dict(changed=changed, current=current)
        else:
            result: dict = dict(changed=changed)

    module.close_client_session()
    module.exit_json(**result)


def validate_params(params: dict, module: MssqlModule) -> None:
    """
    Validates the module parameters.

    Args:
        params (dict): The module parameters.
        module (MssqlModule): The module instance.
    """

    if len(params['permissions']) < 1:
        module.handle_error(MssqlModuleError(message='At least one permission must be specified.'))

    query: str = f"SELECT name FROM sys.server_principals WHERE name = '{params['principal']}'"

    try:
        module.cursor.execute(query)
        result: Optional[dict] = module.cursor.fetchone()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    if result is None:
        module.handle_error(MssqlModuleError(message=f"No server principal exists with the name '{params['principal']}'."))


def get_server_permissions(
        principal: str,
        permissions: list[str],
        module: MssqlModule) -> dict:
    """
    Gets the server-level permissions.

    Args:
        name (str): The name of the SQL Login.
        permissions (list): The server-level permissions.
        module (MssqlModule): The module instance.

    Returns:
        dict: The relevant server-level permissions.
    """

    results: dict = {}

    for permission in permissions:
        results: dict = get_server_permission(principal, permission, module, results)

    return results


def get_server_permission(
        principal: str,
        permission: str,
        module: MssqlModule,
        results: dict) -> dict:
    """
    Gets the server-level permission.

    Args:
        name (str): The name of the SQL Login.
        permission (str): The server-level permission.
        module (MssqlModule): The module instance.
        results (dict): The results of previous operations.

    Returns:
        dict: Results of this and previous operations.
    """

    query: str = f"""
    SELECT principals.name as name,
            permissions.permission_name as permission,
            permissions.state_desc as state
    FROM sys.server_permissions permissions
    JOIN sys.server_principals principals
    ON permissions.grantee_principal_id = principals.principal_id
    WHERE principals.name = '{principal}'
    AND permissions.permission_name = '{convert_permission_to_query(permission)}'
    """

    try:
        module.cursor.execute(query)
        row: Optional[dict] = module.cursor.fetchone()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    if row is None:
        results[permission] = 'revoke'
    else:
        results[permission] = row['state'].lower()

    return results


def convert_permission_to_query(permission: str) -> str:
    """
    Converts the server-level permission to a SQL query.

    Args:
        permission (str): The server-level permission.

    Returns:
        str: The SQL query.
    """

    return permission.replace('_', ' ').upper()


def modify_permission(
        principal: str,
        permission: str,
        previous_state: str,
        state: str,
        module: MssqlModule) -> None:
    """
    Modifies the server-level permission.

    Args:
        name (str): The name of the SQL Login.
        permission (str): The server-level permission.
        previous_state (str): The previous state of the permission.
        state (str): The desired state of the permission.
        module (MssqlModule): The module instance.
    """

    if previous_state == state:
        return

    if state == 'revoke':
        if previous_state == 'grant_with_grant_option':
            query: str = f'REVOKE {convert_permission_to_query(permission)} TO [{principal}] CASCADE;'
        else:
            query: str = f'REVOKE {convert_permission_to_query(permission)} TO [{principal}];'
    elif state == 'grant':
        if previous_state == 'grant_with_grant_option':
            query: str = f'REVOKE GRANT OPTION FOR {convert_permission_to_query(permission)} TO [{principal}] CASCADE;'
        else:
            query: str = f'GRANT {convert_permission_to_query(permission)} TO [{principal}];'
    elif state == 'deny':
        if previous_state == 'grant_with_grant_option':
            query: str = f'DENY {convert_permission_to_query(permission)} TO [{principal}] CASCADE;'
        else:
            query: str = f'DENY {convert_permission_to_query(permission)} TO [{principal}];'
    elif state == 'grant_with_grant_option':
        query: str = f'GRANT {convert_permission_to_query(permission)} TO [{principal}] WITH GRANT OPTION;'

    try:
        module.cursor.execute(query)
        module.conn.commit()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))


def main() -> None:
    run_module()


if __name__ == '__main__':
    main()

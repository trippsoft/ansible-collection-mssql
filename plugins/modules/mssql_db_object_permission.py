#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
module: mssql_db_object_permission
version_added: 1.0.0
author:
  - Jim Tarpley
short_description: Configures a SQL database object-level permission in a Microsoft SQL Server instance.
description:
  - Configures a SQL database object-level permission in a Microsoft SQL Server instance.
attributes:
  check_mode:
    support: full
    details:
      - This module supports check mode.
extends_documentation_fragment:
  - trippsc2.mssql.login
options:
  principal:
    type: str
    required: true
    description:
      - The name of the database user or role for which to configure permissions.
  database:
    type: str
    required: true
    description:
      - The name of the database in which the object exists for which to configure permissions.
  schema:
    type: str
    required: false
    description:
      - The name of the schema in which the object exists for which to configure permissions.
  object:
    type: str
    required: true
    description:
      - The name of the object for which to configure permissions.
  permissions:
    type: list
    required: true
    elements: str
    choices:
      - alter
      - control
      - delete
      - execute
      - insert
      - receive
      - references
      - select
      - take_ownership
      - update
      - view_change_tracking
      - view_definition
    description:
      - The type of database object-level permission to configure.
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
        - The state of the database object-level permission.
"""

EXAMPLES = r"""
- name: Grant SQL database object-level permissions
  trippsc2.mssql.mssql_db_permission:
    login_user: sa
    login_password: password
    login_host: localhost
    user: test
    database: tempdb
    permissions:
      - connect
      - update
    state: grant
    
- name: Deny SQL database object-level permissions
  trippsc2.mssql.mssql_db_permission:
    login_user: sa
    login_password: password
    login_host: localhost
    user: test
    database: tempdb
    permissions:
      - connect
      - update
    state: deny

- name: Grant SQL database object-level permissions with grant option
  trippsc2.mssql.mssql_db_permission:
    login_user: sa
    login_password: password
    login_host: localhost
    user: test
    database: tempdb
    permissions:
      - connect
      - update
    state: grant_with_grant_option

- name: Remove SQL database object-level permissions
  trippsc2.mssql.mssql_db_permission:
    login_user: sa
    login_password: password
    login_host: localhost
    user: test
    database: tempdb
    permissions:
      - connect
      - update
    state: revoke
"""

RETURN = r"""
current:
  type: dict
  returned:
    - success
    - state is C(present)
  description:
    - The configuration of the SQL database object-level permissions.
  sample:
    - permission: connect
      state: grant_with_grant_option
    - permission: update
      state: grant_with_grant_option
  contains:
    permission:
      type: str
      description:
        - The database object-level permission.
    state:
      type: str
      description:
        - The state of the database object-level permission.
previous:
  type: dict
  returned:
    - success
    - changed
  description:
    - The previous configuration of the SQL database object-level permissions.
  sample:
    - permission: connect
      state: grant
    - permission: update
      state: deny
  contains:
    permission:
      type: str
      description:
        - The database object-level permission.
    state:
      type: str
      description:
        - The state of the database object-level permission.
"""

from ..module_utils._mssql_module import MssqlModule
from ..module_utils._mssql_module_error import MssqlModuleError

from ansible.module_utils.common.text.converters import to_native


def run_module():
    module = MssqlModule(
        argument_spec=dict(
            principal=dict(type='str', required=True),
            database=dict(type='str', required=True),
            schema=dict(type='str', required=False),
            object=dict(type='str', required=True),
            permissions=dict(
                type='list',
                required=True,
                elements='str',
                choices=[
                    'alter',
                    'control',
                    'delete',
                    'execute',
                    'insert',
                    'receive',
                    'references',
                    'select',
                    'take_ownership',
                    'update',
                    'view_change_tracking',
                    'view_definition'
                ]
            ),
            state=dict(
                type='str',
                required=False,
                default='grant',
                choices=['grant','deny','grant_with_grant_option','revoke']
            )
        )
    )

    params = module.get_defined_non_connection_params()
    module.initialize_client()
    validate_params(params, module)

    if params.get('schema', None) is None:
        schema = resolve_schema(params['database'], params['object'], module)
    else:
        schema = params['schema']

    previous_permissions = get_db_object_permissions(
        params['principal'],
        params['database'],
        schema,
        params['object'],
        params['permissions'],
        module
    )

    changed = False

    previous = list[dict]()
    current = list[dict]()

    for permission, previous_state in previous_permissions.items():
        if previous_state != params['state']:
            changed = True
        
        if previous_state != 'revoke':
            previous.append(dict(permission=permission, state=previous_state))

        if params['state'] != 'revoke':
            current.append(dict(permission=permission, state=params['state']))

        if not module.check_mode:
            modify_permission(
                params['principal'],
                params['database'],
                schema,
                params['object'],
                permission,
                previous_state,
                params['state'],
                module
            )

    if len(previous) > 0:
        if len(current) > 0:
            result = dict(changed=changed, previous=previous, current=current)
        else:
            result = dict(changed=changed, previous=previous)
    else:
        if len(current) > 0:
            result = dict(changed=changed, current=current)
        else:
            result = dict(changed=changed)

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

    query = f"SELECT name FROM sys.databases WHERE name = '{params['database']}'"

    try:
        module.cursor.execute(query)
        result = module.cursor.fetchone()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    if result is None:
        module.handle_error(MssqlModuleError(message=f"No database exists with the name '{params['database']}'."))

    query = f"""
    SELECT name FROM {params['database']}.sys.database_principals
    WHERE name = '{params['principal']}'
    """

    try:
        module.cursor.execute(query)
        result = module.cursor.fetchone()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    if result is None:
        module.handle_error(MssqlModuleError(message=f"No database principal exists with the name '{params['principal']}'."))

    if params.get('schema', None) is None:
        query = f"SELECT name FROM {params['database']}.sys.objects WHERE name = '{params['object']}'"

        try:
            module.cursor.execute(query)
            result = module.cursor.fetchall()
        except Exception as e:
            module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

        if result is None or len(result) == 0:
            module.handle_error(MssqlModuleError(message=f"No object exists with the name '{params['object']}'."))

        if len(result) > 1:
            module.handle_error(MssqlModuleError(message=f"Multiple objects exist with the name '{params['object']}'. Please specify the schema."))
    else:
        query = f"""
        SELECT objects.name FROM {params['database']}.sys.objects objects
        JOIN {params['database']}.sys.schemas schemas
        ON objects.schema_id = schemas.schema_id
        WHERE objects.name = '{params['object']}'
        AND schemas.name = '{params['schema']}'
        """

        try:
            module.cursor.execute(query)
            result = module.cursor.fetchone()
        except Exception as e:
            module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

        if result is None:
            module.handle_error(MssqlModuleError(message=f"No object exists with the name '{params['object']}' in the schema '{params['schema']}'."))


def resolve_schema(database: str, object: str, module: MssqlModule) -> str:
    """
    Resolves the schema of the database object.

    Args:
        database (str): The name of the database.
        object (str): The name of the object.
        module (MssqlModule): The module instance.

    Returns:
        str: The name of the schema.
    """

    query = f"""
    SELECT objects.name AS name,
            schemas.name AS schema_name
    FROM {database}.sys.objects objects
    JOIN {database}.sys.schemas schemas
    ON objects.schema_id = schemas.schema_id
    WHERE objects.name = '{object}'
    """

    try:
        module.cursor.execute(query)
        result = module.cursor.fetchone()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    return result['schema_name']


def get_db_object_permissions(
        principal: str,
        database: str,
        schema: str,
        object: str,
        permissions: list,
        module: MssqlModule
    ) -> dict:
    """
    Retrieves the database object-level permissions.

    Args:
        principal (str): The name of the principal.
        database (str): The name of the database.
        schema (str): The name of the schema.
        object (str): The name of the object.
        permissions (list): The permissions to retrieve.
        module (MssqlModule): The module instance.

    Returns:
        dict: The database object-level permissions.
    """

    results: dict = dict()

    for permission in permissions:
        results = get_db_object_permission(
            principal,
            database,
            schema,
            object,
            permission,
            module,
            results
        )

    return results


def get_db_object_permission(
        principal: str,
        database: str,
        schema: str,
        object: str,
        permission: str,
        module: MssqlModule,
        results: dict
    ) -> dict:
    """
    Retrieves the database object-level permission.

    Args:
        principal (str): The name of the principal.
        database (str): The name of the database.
        schema (str): The name of the schema.
        object (str): The name of the object.
        permission (str): The permission to retrieve.
        module (MssqlModule): The module instance.
        results (dict): The current results.

    Returns:
        dict: The database object-level permissions.
    """

    query = f"""
    SELECT principals.name AS name,
            permissions.class_desc AS class,
            permissions.permission_name AS permission,
            permissions.state_desc AS state
    FROM {database}.sys.database_permissions permissions
    JOIN {database}.sys.database_principals principals
    ON permissions.grantee_principal_id = principals.principal_id
    JOIN {database}.sys.objects objects
    ON permissions.major_id = objects.object_id
    JOIN {database}.sys.schemas schemas
    ON objects.schema_id = schemas.schema_id
    WHERE principals.name = '{principal}'
    AND objects.name = '{object}'
    AND schemas.name = '{schema}'
    AND permissions.class_desc = 'OBJECT_OR_COLUMN'
    AND permissions.permission_name = '{convert_permission_to_query(permission)}'
    """

    try:
        module.cursor.execute(query)
        row = module.cursor.fetchone()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))
    
    if row is None:
        results[permission] = 'revoke'
    else:
        results[permission] = row['state'].lower()

    return results


def convert_permission_to_query(permission: str) -> str:
    """
    Converts the permission to the query string.

    Args:
        permission (str): The permission to convert.

    Returns:
        str: The query string.
    """

    return permission.replace('_', ' ').upper()


def modify_permission(
        principal: str,
        database: str,
        schema: str,
        object: str,
        permission: str,
        previous_state: str,
        state: str,
        module: MssqlModule
    ) -> None:
    """
    Modifies the database object-level permission.

    Args:
        principal (str): The name of the principal.
        database (str): The name of the database.
        schema (str): The name of the schema.
        object (str): The name of the object.
        permission (str): The permission to modify.
        previous_state (str): The previous state of the permission.
        state (str): The new state of the permission.
        module (MssqlModule): The module instance.
    """
    
    if previous_state == state:
        return
    
    if state == 'revoke':
        if previous_state == 'grant_with_grant_option':
            query = f"""
            USE [{database}];
            REVOKE {convert_permission_to_query(permission)}
                ON OBJECT::{schema}.{object}
                TO [{principal}] CASCADE
            """
        else:
            query = f"""
            USE [{database}];
            REVOKE {convert_permission_to_query(permission)}
                ON OBJECT::{schema}.{object}
                TO [{principal}]
            """
    elif state == 'grant':
        if previous_state == 'grant_with_grant_option':
            query = f"""
            USE [{database}];
            REVOKE GRANT OPTION FOR {convert_permission_to_query(permission)}
                ON OBJECT::{schema}.{object}
                TO [{principal}] CASCADE
            """
        else:
            query = f"""
            USE [{database}];
            GRANT {convert_permission_to_query(permission)}
                ON OBJECT::{schema}.{object}
                TO [{principal}];
            """
    elif state == 'deny':
        if previous_state == 'grant_with_grant_option':
            query = f"""
            USE [{database}];
            DENY {convert_permission_to_query(permission)}
                ON OBJECT::{schema}.{object}
                TO [{principal}] CASCADE
            """
        else:
            query = f"""
            USE [{database}];
            DENY {convert_permission_to_query(permission)}
                ON OBJECT::{schema}.{object}
                TO [{principal}];
            """
    elif state == 'grant_with_grant_option':
        query = f"""
        USE [{database}];
        GRANT {convert_permission_to_query(permission)}
            ON OBJECT::{schema}.{object}
            TO [{principal}] WITH GRANT OPTION
        """

    try:
        module.cursor.execute(query)
        module.conn.commit()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))


def main():
    run_module()


if __name__ == '__main__':
    main()

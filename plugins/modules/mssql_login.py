#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import traceback

try:
    import pymssql
except ImportError:
    HAS_PYMSSQL = False
    PYMSSQL_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_PYMSSQL = True
    PYMSSQL_IMPORT_ERROR = None

from typing import Optional, Union

from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.common.text.converters import to_native

from ..module_utils._mssql_module import MssqlModule
from ..module_utils._mssql_module_error import MssqlModuleError


def run_module():
    module = MssqlModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            type=dict(type='str', required=False, default='sql', choices=['sql', 'windows']),
            state=dict(type='str', required=False, default='present', choices=['present', 'absent']),
            enabled=dict(type='bool', required=False),
            password=dict(type='str', required=False, no_log=True),
            update_password=dict(
                type='str',
                required=False,
                default='always',
                choices=['always', 'on_create'],
                no_log=False
            ),
            login_password_expiration_enabled=dict(type='bool', required=False, no_log=False),
            login_password_policy_enforced=dict(type='bool', required=False, no_log=False)
        )
    )

    if not HAS_PYMSSQL:
        module.fail_json(
            msg=missing_required_lib('pymssql'),
            exception=PYMSSQL_IMPORT_ERROR)

    params = module.get_defined_non_connection_params()
    module.initialize_client()
    validate_params(params, module)

    if params['state'] == 'present':
        result = ensure_present(params, module)
    else:
        result = ensure_absent(params, module)

    module.close_client_session()
    module.exit_json(**result)


def validate_params(params: dict, module: MssqlModule) -> None:
    """
    Validates the parameters for the module.

    Args:
        params: The parameters to validate.
    """

    if params['state'] == 'present':
        if params['type'] != 'sql':
            if 'password' in params:
                module.handle_error(MssqlModuleError('The password parameter is required when state is present and type is not sql.'))

            if 'login_password_expiration_enabled' in params:
                module.handle_error(MssqlModuleError('The login_password_expiration_enabled parameter is not valid for non-SQL logins.'))

            if 'login_password_policy_enforced' in params:
                module.handle_error(MssqlModuleError('The login_password_policy_enforced parameter is not valid for non-SQL logins.'))
        else:
            if params.get('login_password_expiration_enabled', False) and not params.get('login_password_policy_enforced', False):
                module.handle_error(
                    MssqlModuleError(
                        'The login_password_expiration_enabled cannot be true if login_password_policy_enforced parameter is not set to true.'))
    else:
        if 'password' in params:
            module.handle_error(MssqlModuleError('The password parameter is not valid when state is absent.'))

        if 'login_password_expiration_enabled' in params:
            module.handle_error(MssqlModuleError('The login_password_expiration_enabled parameter is not valid when state is absent.'))

        if 'login_password_policy_enforced' in params:
            module.handle_error(MssqlModuleError('The login_password_policy_enforced parameter is not valid when state is absent.'))

    return None


def ensure_present(params: dict, module: MssqlModule) -> Union[dict, MssqlModuleError]:
    """
    Ensures the SQL login is present.

    Args:
        params (dict): The parameters for the module.
        module (MssqlModule): The module object.

    Returns:
        dict: The result of the operation.
    """

    existing_login = get_login(params['name'], module)

    if isinstance(existing_login, MssqlModuleError):
        return existing_login

    if existing_login is None:
        return create_login(params, module)

    return update_login(params, existing_login, module)


def ensure_absent(params: dict, module: MssqlModule) -> Union[dict, MssqlModuleError]:
    """
    Ensures the SQL login is absent.

    Args:
        params (dict): The parameters for the module.
        module (MssqlModule): The module object.

    Returns:
        dict: The result of the operation.
    """

    existing_login = get_login(params['name'], module)

    if isinstance(existing_login, MssqlModuleError):
        return existing_login

    if existing_login is None:
        return dict(changed=False)

    result = dict(
        changed=True,
        previous=existing_login
    )

    if not module.check_mode:
        try:
            module.cursor.execute(f"DROP LOGIN [{params['name']}]")
            module.conn.commit()
        except Exception as e:
            module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    return result


def get_login(name: str, module: MssqlModule) -> Optional[dict]:
    """
    Gets the SQL login by name.

    Args:
        name (str): The name of the SQL login.
        module (MssqlModule): The module object.

    Returns:
        dict: The SQL login.
    """

    query = f"""
    SELECT sp.name as name,
            sp.type as type,
            sp.is_disabled as is_disabled,
            sl.is_policy_checked as is_policy_checked,
            sl.is_expiration_checked as is_expiration_checked
    FROM sys.server_principals sp
    LEFT JOIN sys.sql_logins sl ON sp.principal_id = sl.principal_id
    WHERE sp.name = '{name}'
    """

    try:
        module.cursor.execute(query)
        row: dict | None = module.cursor.fetchone()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    if row is None:
        return None

    return format_login(row, module)


def format_login(row: dict, module: MssqlModule) -> dict:
    """
    Formats the SQL login information returned from SQL Server to match the module.

    Args:
        row (dict): The SQL login information returned from SQL Server.

    Returns:
        dict: The formatted SQL login information.
    """

    if row['type'] == 'S':
        type = 'sql'
    elif row['type'] == 'U':
        type = 'windows'
    elif row['type'] == 'G':
        type = 'windows'
    elif row['type'] == 'C':
        type = 'certificate'
    elif row['type'] == 'E':
        type = 'azure'
    elif row['type'] == 'X':
        type = 'azure'
    elif row['type'] == 'K':
        type = 'asymmetric_key'
    else:
        module.handle_error(MssqlModuleError('Existing login has unknown type: %s' % row))

    return dict(
        name=row['name'],
        type=type,
        enabled=not row['is_disabled'],
        login_password_expiration_enabled=row['is_expiration_checked'],
        login_password_policy_enforced=row['is_policy_checked']
    )


def create_login(params: dict, module: MssqlModule) -> dict:
    """
    Creates the SQL login.

    Args:
        params (dict): The parameters for the module.
        module (MssqlModule): The module object.

    Returns:
        dict: The result of the operation.
    """

    if params['type'] == 'sql':
        current = dict(
            name=params['name'],
            type=params['type'],
            enabled=params.get('enabled', True),
            login_password_expiration_enabled=params.get('login_password_expiration_enabled', False),
            login_password_policy_enforced=params.get('login_password_policy_enforced', True))
    else:
        current = dict(
            name=params['name'],
            type=params['type'],
            enabled=params.get('enabled', True)
        )

    result = dict(
        changed=True,
        password_set=params.get('password') is not None,
        current=current
    )

    if not module.check_mode:
        if params['type'] == 'sql':

            if current['login_password_expiration_enabled']:
                login_password_expiration_enabled_value = 'ON'
            else:
                login_password_expiration_enabled_value = 'OFF'

            if current['login_password_policy_enforced']:
                login_password_policy_enforced_value = 'ON'
            else:
                login_password_policy_enforced_value = 'OFF'

            query = f"""
            CREATE LOGIN [{params['name']}]
                WITH PASSWORD = '{params['password']}',
                    CHECK_EXPIRATION = {login_password_expiration_enabled_value},
                    CHECK_POLICY = {login_password_policy_enforced_value}
            """
        elif params['type'] == 'windows':
            query = f"CREATE LOGIN [{params['name']}] FROM WINDOWS"
        try:
            module.cursor.execute(query)
            module.conn.commit()

            if not params.get('enabled', True):
                module.cursor.execute(f"ALTER LOGIN [{params['name']}] DISABLE")
                module.conn.commit()
        except Exception as e:
            module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    return result


def update_login(params: dict, existing_login: dict, module: MssqlModule) -> Union[dict, MssqlModuleError]:
    """
    Updates the SQL login.

    Args:
        params (dict): The parameters for the module.
        existing_login (dict): The existing SQL login.
        module (MssqlModule): The module object.

    Returns:
        dict: The result of the operation.
    """

    if params['type'] != existing_login['type']:
        module.handle_error(MssqlModuleError('Cannot change login type. Remove the existing login first and then create it with the new type.'))

    enabled_changed = params.get('enabled', existing_login['enabled']) != existing_login['enabled']

    if params['type'] == 'sql':
        current = dict(
            name=params['name'],
            type=params['type'],
            enabled=params.get('enabled', existing_login['enabled']),
            login_password_expiration_enabled=params.get('login_password_expiration_enabled', existing_login['login_password_expiration_enabled']),
            login_password_policy_enforced=params.get('login_password_policy_enforced', existing_login['login_password_policy_enforced'])
        )

        password_set = params['update_password'] == 'always'
        login_password_expiration_enabled_changed = current['login_password_expiration_enabled'] != existing_login['login_password_expiration_enabled']
        login_password_policy_enforced_changed = current['login_password_policy_enforced'] != existing_login['login_password_policy_enforced']
    else:
        current = dict(
            name=params['name'],
            type=params['type'],
            enabled=params.get('enabled', existing_login['enabled'])
        )

        password_set = False
        login_password_expiration_enabled_changed = False
        login_password_policy_enforced_changed = False

    config_changed = enabled_changed or login_password_expiration_enabled_changed or login_password_policy_enforced_changed
    changed = password_set or config_changed

    result = dict(
        changed=changed,
        password_set=password_set,
        current=current
    )

    if config_changed:
        result['previous'] = existing_login

    if not module.check_mode:
        if enabled_changed:
            if params.get('enabled', existing_login['enabled']):
                query = f"ALTER LOGIN [{params['name']}] ENABLE"
            else:
                query = f"ALTER LOGIN [{params['name']}] DISABLE"

            try:
                module.cursor.execute(query)
                module.conn.commit()
            except Exception as e:
                module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

        if login_password_policy_enforced_changed:
            query = f"""
            ALTER LOGIN [{params['name']}]
                WITH CHECK_POLICY = {'ON' if current['login_password_policy_enforced'] else 'OFF'}
            """

            try:
                module.cursor.execute(query)
                module.conn.commit()
            except Exception as e:
                module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

        if login_password_expiration_enabled_changed:
            query = f"""
            ALTER LOGIN [{params['name']}]
                WITH CHECK_EXPIRATION = {'ON' if current['login_password_expiration_enabled'] else 'OFF'}
            """

            try:
                module.cursor.execute(query)
                module.conn.commit()
            except Exception as e:
                module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

        if password_set:
            query = f"ALTER LOGIN [{params['name']}] WITH PASSWORD = '{params['password']}'"

            try:
                module.cursor.execute(query)
                module.conn.commit()
            except Exception as e:
                module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    return result


def main():
    run_module()


if __name__ == '__main__':
    main()

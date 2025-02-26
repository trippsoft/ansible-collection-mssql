# Changelog

All notable changes to this project will be documented in this file.

## [1.3.3] - 2025-02-13

### Module Plugin - mssql_db_object_permission

- Reverted changing documentation from .py file to .yml file because ansible-lint does not parse it correctly yet.

### Module Plugin - mssql_db_permission

- Reverted changing documentation from .py file to .yml file because ansible-lint does not parse it correctly yet.

### Module Plugin - mssql_db_user

- Reverted changing documentation from .py file to .yml file because ansible-lint does not parse it correctly yet.

### Module Plugin - mssql_login

- Reverted changing documentation from .py file to .yml file because ansible-lint does not parse it correctly yet.

### Module Plugin - mssql_server_permission

- Reverted changing documentation from .py file to .yml file because ansible-lint does not parse it correctly yet.

## [1.3.2] - 2025-02-09

### Module Plugin - mssql_db_object_permission

- Made various changes for code quality and style improvements suggested by Ansible sanity tests.

### Module Plugin - mssql_db_permission

- Made various changes for code quality and style improvements suggested by Ansible sanity tests.

### Module Plugin - mssql_db_user

- Made various changes for code quality and style improvements suggested by Ansible sanity tests.

### Module Plugin - mssql_login

- Made various changes for code quality and style improvements suggested by Ansible sanity tests.

### Module Plugin - mssql_server_permission

- Made various changes for code quality and style improvements suggested by Ansible sanity tests.

## [1.3.1] - 2025-01-08

### Collection

- Added Changelog.
- Updated collection README documentation.

## [1.3.0] - 2024-11-21

### Role - install

- Added `retries` to the step to setup AD keytab file on Linux.

## [1.1.3] - 2024-09-23

### Collection

- Added requirements.txt file to allow execution environments to automatically acquire the `pymssql` Python module.

## [1.1.2] - 2024-09-23

### Role - install

- Fixed incorrect task name.

## [1.1.1] - 2024-09-23

### Role - install

- Changed the `mssql_vault_manage_monitoring_credentials` variable to default to disabled.

## [1.1.0] - 2024-09-23

### Role - install

- Added the `mssql_vault_manage_sa_password` variable to enable/disable (enabled by default) managing the SA password in HashiCorp Vault.
- Added the `mssql_vault_sa_mount_point` and `mssql_vault_sa_secret_path` variable to configure where the SA password is stored.

## [1.0.2] - 2024-09-23

### Role - install

- Removed the option to omit the `mssql_password` variable.

## [1.0.1] - 2024-09-23

### Role - install

- Added default values for the `mssql_host`, `mssql_user`, and `mssql_password` variables that use the default SA credentials to connect to the server.

## [1.0.0] - 2024-09-23

### Collection

- Initial release.
- *mssql_db_object_permission* module plugin added.
- *mssql_db_permission* module plugin added.
- *mssql_db_user* module plugin added.
- *mssql_login* module plugin added.
- *mssql_server_permission* module plugin added.
- *install* role added.

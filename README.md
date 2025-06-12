# Ansible Collection: trippsc2.mssql

This collection contains modules and roles for installing and configuration Microsoft SQL Server.

## Content

### Module plugins

- [mssql_db_object_permission](plugins/modules/mssql_db_object_permission.py) - Configures a SQL database object-level permission in a Microsoft SQL Server instance.
- [mssql_db_permission](plugins/modules/mssql_db_permission.py) - Configures a SQL database-level permission in a Microsoft SQL Server instance.
- [mssql_db_user](plugins/modules/mssql_db_user.py) - Configures a SQL database user in a Microsoft SQL Server instance.
- [mssql_login](plugins/modules/mssql_login.py) - Configures a SQL Login in a Microsoft SQL Server instance.
- [mssql_server_permission](plugins/modules/mssql_server_permission.py) - Configures a SQL server-level permission in a Microsoft SQL Server instance.

### Roles

- [install](roles/install/README.md) - This role installs Microsoft SQL Server.

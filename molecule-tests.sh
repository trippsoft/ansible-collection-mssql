#! /bin/bash

set -e

molecule test -s mssql_login_sql
molecule test -s mssql_server_permission
molecule test -s mssql_db_user
molecule test -s mssql_db_permission
molecule test -s mssql_db_object_permission

MOLECULE_BOX="rocky8_cis" molecule test -s mssql_login_windows
MOLECULE_BOX="ubuntu2204_base" molecule test -s mssql_login_windows
MOLECULE_BOX="rocky9_base" molecule test -s mssql_login_windows
MOLECULE_BOX="ubuntu2004_base" molecule test -s mssql_login_windows

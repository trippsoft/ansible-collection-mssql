#! /bin/bash

set -e

MOLECULE_BOX="rocky8_cis" MOLECULE_MSSQL_VERSION="2019" molecule test -s linux
MOLECULE_BOX="w2022_cis" MOLECULE_MSSQL_VERSION="2019" molecule test -s win
MOLECULE_BOX="ubuntu2004_base" MOLECULE_MSSQL_VERSION="2019" molecule test -s linux

MOLECULE_BOX="w2019_cis" MOLECULE_MSSQL_VERSION="2019" molecule test -s win
MOLECULE_BOX="w2025_base" MOLECULE_MSSQL_VERSION="2019" molecule test -s win

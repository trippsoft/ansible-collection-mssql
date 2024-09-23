#! /bin/bash

set -e

MOLECULE_BOX="w2019_cis" MOLECULE_MSSQL_VERSION="2016" molecule test -s win

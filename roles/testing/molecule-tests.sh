#! /bin/bash

set -e

MOLECULE_BOX="rocky8_cis" molecule test -s linux
MOLECULE_BOX="ubuntu2204_base" molecule test -s linux

MOLECULE_BOX="rocky9_base" molecule test -s linux
MOLECULE_BOX="ubuntu2004_base" molecule test -s linux

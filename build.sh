#!/usr/bin/env bash

python setup.py sdist

VENVS=~/venvs
WORKING=`pwd`

cd $VENVS
python -m venv testapp
cd testapp
. bin/activate
pip install -U setuptools
pip install -U pip
pip install "$WORKING/dist/clldmpg-$1.tar.gz"
pcreate -t clldmpg_app testapp
cd testapp
pip install -e .[test]
python testapp/scripts/initializedb.py development.ini
pytest
cd $VENVS
rm -rf testapp

#!/usr/bin/env bash
VENVS=~/venvs

cd $VENVS/cheesecake
. bin/activate
pip install -U setuptools
cd clldmpg
git checkout master
git pull origin master
python setup.py sdist
cheesecake_index --path="dist/clldmpg-$1.tar.gz" --with-pep8

cd $VENVS
virtualenv testapp
cd testapp
. bin/activate
pip install -U setuptools
pip install -U pip
pip install "$VENVS/cheesecake/clldmpg/dist/clldmpg-$1.tar.gz"
pcreate -t clldmpg_app testapp
cd testapp
pip install -e .[test]
python testapp/scripts/initializedb.py development.ini
pytest
cd $VENVS
rm -rf testapp


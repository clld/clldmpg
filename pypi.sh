VENVS=~/venvs

cd $VENVS/pypi
. bin/activate
cd clldmpg
git pull origin
git checkout tags/v$1
python setup.py sdist register upload


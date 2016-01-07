VENVS=~/venvs

cd $VENVS/cheesecake
. bin/activate
cd clldmpg
git checkout master
git pull origin master
python setup.py sdist
cheesecake_index --path="dist/clldmpg-$1.tar.gz" --with-pep8

cd $VENVS
virtualenv testapp
cd testapp
. bin/activate
pip install "$VENVS/cheesecake/clldmpg/dist/clldmpg-$1.tar.gz"
pcreate -t clldmpg_app testapp
cd testapp
python setup.py develop
python testapp/scripts/initializedb.py development.ini
pip install nose
pip install mock==1.1
nosetests
cd $VENVS
rm -rf testapp

Releasing clldmpg
=================

- Do platform test via tox:
```
tox -r
```

- Make sure all scaffold tests pass:
```
./venvs/clld/clldmpg/build.sh "<prev-rel-no>"
```

- Change `setup.py` version to the new version number.

- Bump version number:
```
git commit -a -m"bumped version number"
```

- Create a release tag:
```
git tag -a v0.2 -m"first version to be released on pypi"
```

- Push to github:
```
git push origin
git push --tags
```

- Release to PyPI
```
git checkout tags/v$1
rm dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
```
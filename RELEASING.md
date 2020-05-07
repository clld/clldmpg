Releasing clldmpg
=================

- Do platform test via tox:
```
tox -r
```

- Change `setup.py` version to the new version number.

- Bump version number:
```
git commit -a -m"Release <version number>"
```

- Create a release tag:
```
git tag -a v0.2 -m"first version to be released on pypi"
```

- Release to PyPI
```
git checkout tags/v$1
python setup.py clean --all
rm dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
```

- Change `setup.py` version to the new version number.

- Set version number for next development cycle:
```
git commit -a -m"bumped version number"
```

- Push to github:
```
git push origin
git push --tags
```

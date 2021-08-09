pdoc --html --force --output-dir --template-dir docs/templates docs .
python -m build
python -m twine upload --repository --skip-existing testpypi dist/*
python -m twine upload --repository --skip-existing pypi dist/*
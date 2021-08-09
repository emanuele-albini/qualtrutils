pdoc --html --force --output-dir --template-dir docs/templates docs .
python -m build
python -m twine upload --repository testpypi dist/*
python -m twine upload --repository pypi dist/*
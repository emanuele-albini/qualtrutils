pdoc --html --force --output-dir docs --template-dir docs/templates .
python -m build
python -m twine upload --repository testpypi --skip-existing dist/*
python -m twine upload --repository pypi --skip-existing dist/*
# tags: deploy, ship, pypi

# If this is your first time or it's just been a while:
# https://packaging.python.org/guides/using-testpypi/
# https://packaging.python.org/tutorials/distributing-packages/#uploading-your-project-to-pypi

# rm -rf dist/
# python 2
# python setup.py bdist_wheel
# switch to python 3 and run it again
# python setup.py bdist_wheel

# Test
twine upload -r testpypi --config-file .pypirc dist/*

# Prod
twine upload --config-file .pypirc dist/*

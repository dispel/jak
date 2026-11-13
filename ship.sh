#!/bin/sh
# How to release a new version of jak to PyPI.
#
# Run this from the repo root, on an up to date master with green CI:
#
#   sh ship.sh
#
# It builds the package, checks it and uploads it to TestPyPI. Nothing is
# published to the real PyPI by this script; the last steps are printed at the
# end for you to run by hand.
#
# Before you run it:
#   1. Set __version__ in jak/__init__.py (https://semver.org/).
#   2. In docs/changelog.rst, set the release date of the new version and the
#      end date of the previous one.
#   3. Get that merged to master.
#   4. Have a .pypirc in the repo root (it is gitignored) with API tokens for
#      [pypi] and [testpypi]. See https://packaging.python.org/en/latest/specifications/pypirc/

set -eu

version=$(python3 -c "import jak; print(jak.__version__)")
echo "Shipping jak $version"

python3 -m pip install --quiet --upgrade build twine

# Old builds in dist/ would get uploaded too.
rm -rf dist build
python3 -m build
python3 -m twine check dist/*
python3 -m twine upload -r testpypi --config-file .pypirc dist/*

cat <<DONE

jak $version is on TestPyPI. Try it in a fresh virtualenv:

  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ jak==$version
  jak --version

If it works, publish it and tag the release:

  python3 -m twine upload --config-file .pypirc dist/*
  git tag $version && git push origin $version
  gh release create $version --title v$version --notes "See docs/changelog.rst"
DONE

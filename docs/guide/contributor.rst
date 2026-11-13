.. _contributor:


Contributor information
=======================

Just like with jaks functionality we've worked hard to make developer installation consistent and easy. It should always be quick for people to contribute and the tests should help people know whether their
changes work or not BEFORE they open a PR.

We aim to be friendly to rookie devs, so if you are in doubt about proper operating procedure don't hesitate to reach out by creating an `issue <https://github.com/dispel/jak/issues>`_, we are super friendly =).


Developer machine setup
-----------------------

You need git and a :ref:`supported version of Python <support_detailed>`. Clone this repo, then from its root:

.. sourcecode:: shell

  # Create and activate a virtualenv
  python3 -m venv .venv
  source .venv/bin/activate

  # Install jak in editable mode, plus the tools used for development
  pip install --editable . -r requirements_dev.txt

  # Run the tests
  pytest


Notes of import
---------------

You only need one Python version locally. When you open a pull request, GitHub Actions runs the tests on every supported version (see ``.github/workflows/test.yml``).


Updating documentation
----------------------

Documentation is important because it helps people understand jak. We welcome spelling, grammar, and generally any improvements to the documentation that help people understand jak and stay secure.

jak uses `sphinx <http://www.sphinx-doc.org/>`_ to generate documentation.

To update the docs edit the ``*.rst`` file that has the information you want to improve upon and then:

.. sourcecode:: shell

  # from the root of jak, with the virtualenv active
  cd docs

  # clean out previous version and remake the html
  rm -rf _build && make html

Inspect the new docs by simply double clicking ``docs/_build/html/index.html`` to open it in your browser.


Pull requests
-------------

Once your branch or fork looks good make a PR and one of the stewards will take a look at it and give you a review (and hopefully merge it!).


Alerts
------

No alerts. Everything seems to be working fine.


Future versions
---------------

0 - 10 are the formative years. If we get past them (which seems frankly highly unlikely) we will start a new naming scheme. We use `semantic versioning <http://semver.org/>`_ so the only time we shift the first number would be if we make backwards incompatible changes. The exception to this is 1.0 which will be assigned when Chris DiLorenzo thinks jak is (1) verified to be secure and (2) have no known bugs and (3) have decent tests for it‘s core functionality.

.. sourcecode:: text

  0.X Troubled Toddler
  1.X Young Whippersnapper  <-- CURRENT
  2.X Teenage Wasteland
  3.X High school Sweetheart
  4.X Wannabe Scientist
  5.X Jaded Hipster
  6.X Midlife Maniac
  7.X Dorky Parent
  8.X Rattled Retiree
  9.X Cranky Old Seafarer
  10.X Wizened Witch

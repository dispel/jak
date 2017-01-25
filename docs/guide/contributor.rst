.. _contributor:


Contributor information
=======================

Just like with jaks functionality we've worked hard to make developer installation consistent and easy. It should always be quick for people to contribute and the tests should help people know whether their
changes work or not BEFORE they open a PR.

We aim to be friendly to rookie devs, so if you are in doubt about proper operating procedure don't hesitate to reach out by creating an `issue <https://github.com/dispel/jak/issues>`_, we are super friendly =).


Developer machine setup
-----------------------

1. Clone this repo
2. Install the excellent [vagrant](https://www.vagrantup.com/)
3. See below.

.. sourcecode:: shell

  # Boot up the vagrant machine
  # This will run for quite some time, I HIGHLY recommend looking at the Vagrantfile
  # for a description of what is happening.
  vagrant up

  # Enter sandman
  vagrant ssh

  # This is where the project files are mirrorer on the virtual machine
  cd /vagrant

  # Choose a virtualenv to work on (see virtualenvwrapper docs)
  # It is recommended you use the py27 environment for development and
  # then switching to py35 when you have an issue in Python 3.
  workon py27

  # Run tests for multiple Python versions (see tox.ini)
  tox

  # Or run tests in just the current environment
  pytest


Notes of import
---------------

To edit which environments the tests should be run as see the `tox.ini` file.
We would prefer to be developing against Python 3 but the reality is that it is easier to dev against Python 2 and continually make sure it also works for 3.


Updating documentation
----------------------

Documentation is important because it helps people understand jak. We welcome spelling, grammar, and generally any improvements to the documentation that help people understand jak and stay secure.

jak uses `sphinx <http://www.sphinx-doc.org/>`_ to generate documentation.

To update the docs edit the ``*.rst`` file that has the information you want to improve upon and then:

.. sourcecode:: shell

  # from the root of jak, probably /vagrant
  cd docs

  # clean out previous version and remake the html
  rm -rf _build && make html

Inspect the new docs by simply double clicking ``docs/_build/html/index.html`` to open it in your browser.


Pull requests
-------------

Once your branch or fork looks good make a PR and one of the stewards will take a look at it and give you a review (and hopefully merge it!).


Alerts
------

It currently (2017-01-25) appears that tox will NOT run from Python 3.6 due to urrlib3 not existing. So run your tox from a different base Python environment for now.

Also PyPy tests don't seem to run in tox either, I recommend checking out the virtualenv (``workon pypy``) and running them straight with ``pytest``. If someone could fix this, it would be much appreciated.


Future versions
---------------

0 - 10 are the formative years. If we get past them (which seems frankly highly unlikely) we will start a new naming scheme. We use `semantic versioning <http://semver.org/>`_ so the only time we shift the first number would be if we make backwards incompatible changes. The exception to this is 1.0 which will be assigned when Chris DiLorenzo thinks jak is (1) verified to be secure and (2) have no known bugs and (3) have decent tests for it's core functionality.

.. sourcecode:: text

  0.X Troubled Toddler        <-- CURRENT
  1.X Young Whippersnapper
  2.X Teenage Wasteland
  3.X Highschool Sweetheart
  4.X Wannabee Scientist
  5.X Jaded Hipster
  6.X Midlife Maniac
  7.X Dorky Parent
  8.X Rattled Retiree
  9.X Cranky Old Seafarer
  10.X Wizened Witch

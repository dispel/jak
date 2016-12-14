# Contributor readme

Just like with jaks functionality we've worked hard to make developer installation consistent and easy.
It should always be quick for people to contribute and the tests should help people know whether their
changes work or not BEFORE they open a PR.

We aim to be friendly to rookie devs, so if you are in doubt about proper operating procedure don't hesitate to reach out by creating an issue, we are super friendly =).

1. Clone this repo
2. Install the excellent [vagrant](https://www.vagrantup.com/)
3. See below.

```
# Boot up the vagrant machine
# This will run for quite some time, I HIGHLY recommend looking at the Vagrantfile
# for a description of what is happening.
vagrant up

# Enter sandman
vagrant ssh

# This is where the project files are mirrorer on the virtual machine
cd /vagrant

# Choose a virtualenv to work on, the the following two are pre-created
# py27 --> python 2.7.6
# py35 --> python 3.5.2
# It is recommended you use py27 for development and then switching to py35 when
# you have an issue in python 3.
workon py27

# Run the tests (see tox.ini)
tox

# Or run tests in just the current environment
pytest

# $$$ Profit $$$
# Let us know if you have any issues.
```

## Notes of import

To edit which environments the tests should be run as see the `tox.ini` file.
We would prefer to be developing against python 3 but the reality is that it is easier to dev against python 2 and continually make sure it also works on 3. Eventually we will deprecate python 2.7 compatibility. Probably when it reaches end of life


# Future versions

0 - 10 are the formative years. If we get past them we will start
a new naming scheme. We use semantic naming so the only time we shift
the first number would be if we make backwards incompatible changes.
```
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
```

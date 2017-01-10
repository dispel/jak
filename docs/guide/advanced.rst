.. _advanced:

Advanced usage
==============

Here we answer questions not many people will have.

What is in the .jak folder?
---------------------------

The .jak folder holds the auto generated key that jak uses in the ``keyfile`` (link).


How does jak perform the diffing at a merge conflict?
-----------------------------------------------------
TODO

Is jaks encryption strong (AES-256)?
------------------------------------
TODO

How does the pre-commit hook work?
TODO

Encryption
----------

jak uses AES256 which is secure (source) as long as you feed it a good password. jak will generate this password for you if you ask nicely.

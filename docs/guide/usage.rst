.. _usage:

Basic usage
===========


Getting started
---------------

jak is intended for developers who want to protect secret files (such as .env files) in their shared git repositories. However there is nothing stopping jak from being instantiated into any folder nor encrypting any text file.

Let's say we have the project ``flowers`` which has two secret files we want to protect, ``/flowers/.env and /flowers/settings/keys``.

.. sourcecode:: shell

   $> cd /path/to/flowers

   $> jak start

   # edit the jakfile to look like this
   # {
   #    "files_to_encrypt": [".env", "settings/keys"],
   #    "keyfile": ".jak/keyfile"
   # }

   $> jak encrypt all

   # you can also do it one by one
   $> jak decrypt .env

Easy peasy lemon squeeze! :ref:`Read more about initializing jak here. <start_cmd>`


Which jak files can be committed?
---------------------------------

**commit:** jakfile

**ignore:** .jak folder (which by default includes the keyfile), the keyfile (if you don't have it in your .jak folder).

**NEVER EVER COMMIT YOUR KEYFILE! IT IS WHAT ENCRYPTS/DECRYPTS YOUR SECRETS!**


.. _keyfile:

keyfile
-------

The keyfile is optional, as you can always pass through a key if you wish.


.. _jakfile:

jakfile
-------

A jakfile holds the common settings when issuing jak commands from the current working directory that has the jakfile in it.

.. sourcecode:: json

   {
      "files_to_encrypt": ["file1", "dir/file2"],
      "keyfile": "/path/to/keyfile"
   }

A jakfile has two values in it: ``"files_to_encrypt"`` and ``"keyfile"``.

The ``keyfile`` value is optional as you can supply a key or a different keyfile manually as an optional argument. It should point to where your keyfile is located either absolutely or relatively to the location of the jakfile.
We recommend using the ``keyfile`` value in the jakfile due to it (1) being easier and (2) not being less secure than supplying it as a command.

**You should switch your key and cycle all of your secrets if you computer is compromised.**

The ``files_to_encrypt`` value is a list specifying the files you wish to encrypt. This serves two purposes:

1. If you are in a git repository and have added the :ref:`pre-commit hook <start_cmd>` the hook will check against this list to identify whether you are adding a secret file in its decrypted state, and if so encrypt it for you.
2. It allows you to use the ``jak stomp/shave`` commands for encrypting and decrypting all of the files in the list really easily.

.. _diffing:

Diffing
-------

:ref:`Reference on the diff command. <diff_cmd>`

The file being diffed should have a conflict looking something like this:

.. sourcecode:: text

  <<<<<<< HEAD
  ZDRiM2Q0Yjg0ZTFkNDg3NzRhOTljOWVmYjAxOTE4NmI4Y2UzMTkwNTM5N2Nj
  YjdiYmQyZDU3MjI1MDkwY2ExYmU0NTMzOGYxYTViY2I0YWNlYzdmOWM2OTgz
  NmI5ODkxOWNhNjc5YjdiNGQ5ZDJiMTYyNDFhMzcwMWYxNDVmMWO8ttnsUSsa
  iDNgzDF18NB5RMHOOxjt13wRdV_RHxtZgw==
  =======
  MGUwMWJhYjgxNDcyMjY2MjhmMzMzNWFlYTMwZDYzYzc5ZDc0NzVhMDc0M2Ji
  ZWUyMDc2NTAyZWM5MTRkMzQ5MmU4NTBlYzY1YjlmYTUwYTdlN2M2MDg3ZTI4
  NGMxNDZjYzJiZDczNGE1ZDEzYmRkZDMyY2IwMDI5Mjc3MWJmOWNXRvFeiNn8
  b6JFJwpATrZOE2srs1sc3p2TM529sw-11Q==
  >>>>>>> f8eb651525b7403aa5ed93c251374ddef8796dee

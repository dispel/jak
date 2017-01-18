.. _usage:

Basic usage
===========



Installation
------------

Assuming you :ref:`fullfill the basic support requirements <support_short>` all you need to do is ``pip install jak``.



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

   # you can also encrypt/decrypt specific files
   $> jak decrypt .env

Easy peasy lemon squeeze! :ref:`Read more about initializing jak here. <start_cmd>`



Using jak without a jakfile
---------------------------

Heres a video that explains:

* Using jak without setup (which is fine, but not recommended for teams).
* Generating a secure key.
* Using the key to encrypt/decrypt a file via the CLI.
* Creating your own keyfile.
* One thing I do want to highlight is that the key will be stored in your CLI history, so this is not inherently more secure than keeping the key in a keyfile.


.. raw:: html

   <asciinema-player src="/_static/videos/nosetup.json"></asciinema-player>


Which jak files should be committed?
------------------------------------

**commit:** jakfile

**ignore:** .jak folder (which by default includes the keyfile)

**NEVER EVER COMMIT YOUR KEYFILE! IT IS WHAT ENCRYPTS/DECRYPTS YOUR SECRETS!**



.. _keyfile:

keyfile
-------

The keyfile is optional, as you can always pass through a key if you wish. This means you can store the key somewhere else if you are worried about having it in plaintext, in a file, on your computer. Which is a really bad idea if someone else has access to your computer, or you suspect your computer has been in some other way compromised. However, since you do need to use the key in some fashion to decrypt/encrypt files with jak an argument can definitely be made that having it in a file as opposed to having it in your command history (``$> history``) is about the same level of security. Passing keys to jak in a more secure way is something we are actively thinking about, and if you have opinions you should get in touch.

A Keyfile can be referenced from the jakfile (see below) or directly ``jak encrypt --keyfile /path/to/keyfile``.

The keyfile should have NO INFORMATION other than a :ref:`secure key <key>`.



.. _key:

key
---

Generate a new key by issuing the :ref:`jak keygen <keygen_cmd>` command.

Since jak generates a key 32 byte key (64 characters, which jak generates as `Nibbles <https://en.wikipedia.org/wiki/Nibble>`_ (4bit) to keep things easy to read. If you really know what you are doing there is nothing stopping you from feeding jak 64 characters where each is a full byte though, so you could theoretically go for AES512 under this scheme.




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

Here is a video for your viewing pleasure.

.. raw:: html

   <asciinema-player src="/_static/videos/diffmerge_short.json"></asciinema-player>

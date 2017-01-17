.. _commands:

Command reference
=================

Commands are given in the format ``jak <COMMAND> <ARGUMENTS> <OPTIONS>``. Some example commands:

.. sourcecode:: shell

   jak --help
   jak start
   jak keygen
   jak keygen -m
   jak encrypt file
   jak encrypt file --key 64af685c12bf9f2245b851c528bdd6f41e351c8dbe614db4ea81d3486fc0ee5c
   jak decrypt file --keyfile secrets/jak/keyfile
   jak encrypt all
   jak stomp
   jak decrypt all
   jak shave
   jak diff



--help
------

``jak <OPTIONAL COMMAND> --help``

More information about jak or a jak command.

``jak == jak -h == jak --help``

``jak <COMMAND> -h == jak <COMMAND> --help``



--version, -v
-------------

``jak -v``

Prints out the version.



.. _start_cmd:

start
-----

``jak start``

Initializes jak into your current working directory.

**We highly recommend running this in the root of a git repository.**

Specifically it will:

- Add a hidden ``.jak`` directory
- Add a :ref:`jakfile <jakfile>`.
- Add a :ref:`keyfile <keyfile>` (with a generated random 32 byte password in it) inside the ``.jak`` directory.
- Check if it is being run in a in a git repository

  - IF GIT: it will ask if you want to add a pre-commit hook for auto encrypting files which are specified in the ``"file_to_encrypt"`` value in the :ref:`jakfile <jakfile>` IF you should accidentally try to commit them.
  - IF GIT: It will add the ``.jak`` folder to the ``.gitignore``.

It should give you very detailed output about what is happening.

The start command is idempotent, so you can run it many times if you (for example) on second thought would like to add the git pre-commit hook.



encrypt
-------

``jak encrypt <FILE> <OPTIONS>`` or ``jak encrypt all``.

The ``all`` command requires a :ref:`jakfile <jakfile>` to exist, and will encrypt all files that are designated in the ``"files_to_encrypt"`` value.

**optional arguments:**

.. sourcecode:: text

   -k, --key
      jak encrypt <FILE> -k <KEY>

   -kf, --keyfile
      jak encrypt <FILE> -kf <PATH TO KEYFILE THAT MUST HAVE A 32 BYTE KEY IN IT>



decrypt
-------

``jak decrypt <FILE> <OPTIONS>`` or ``jak decrypt all``.

The ``all`` command requires a :ref:`jakfile <jakfile>` to exist, and will decrypt all files that are designated in the ``"files_to_encrypt"`` value.

**optional arguments:**

.. sourcecode:: text

   -k, --key
      jak decrypt <FILE> -k <KEY>

   -kf, --keyfile
      jak decrypt <FILE> -kf <PATH TO KEYFILE THAT MUST HAVE A 32 BYTE KEY IN IT>



.. _keygen_cmd:

keygen
------

Generate a 32byte key that jak will accept. Returns it to the command line.

**optional arguments:**

.. sourcecode:: text

   -m, --minimal
      Makes the command only return the key with no comments



.. _diff_cmd:

diff
----

``jak diff <FILE> <OPTIONS>``

This command will decrypt the LOCAL and REMOTE parts of a merge conflict.

It will then prompt you for if you want to open the conflict in a merge tool
such as vimdiff or opendiff (default on macOS) or if you simply want the decrypted content written back into the file
so you can solve it yourself using your favorite text editor.

:ref:`Read more here. <diffing>`



stomp
-----

``jak stomp``

Alias for ``jak encrypt all``.

**Has the same options as the encrypt/decrypt commands.**



shave
-----

``jak shave``

Alias for ``jak decrypt all``.

**Has the same options as the encrypt/decrypt commands.**

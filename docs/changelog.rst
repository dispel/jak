.. _changelog:


Changelog
=========


1.0 (Young Whippersnapper)
--------------------------

Lifecycle: Not released yet.

1.0.0 Will be assigned when we have verified that the encryption is absolutely stable AND we believe the risk of us accidentally deleting peoples secrets is < 0.0001%. In practice this means better unit testing and talking to 2-3 more cryptography experts (especially outside of Dispel). Are you such an expert? Get in touch! cdilorenzo@dispel.io.


0.14.6
------

Lifecycle: unreleased

* **[0.14.6]** BUG: Had issue when double decrypting certain files (which should be safe operation, and now it is again). `(PR#56) <https://github.com/dispel/jak/pull/56>`_


0.14.5
------

Lifecycle: 2018-03-08 - current

* **[0.14.4]** BUG: SourceTree (and other linuxy apps hopefully) should now work with the pre-commit hook. `(PR#45) <https://github.com/dispel/jak/pull/45>`_
* **[0.14.5]** ENHANCEMENT: Better message when malformed jakfile. `(PR#51) <https://github.com/dispel/jak/pull/51>`_

* Other:
  * Updated 2017 to 2018 (Happy new year!?)
  * Removed formal support for python 3.3 (since it is at its end of life).


0.14.3
------

Lifecycle: 2017-09-02

* **[0.14.2]** BUG: Files with the same name now support the backup feature (maintain their encrypted state if their unencrypted state is not edited on re-encryption) if they are in different folders. `(PR#40) <https://github.com/dispel/jak/pull/40>`_
* **[0.14.3]** DEV: Improved one of our tests that was placing backup files where they did not belong. `(PR#42) <https://github.com/dispel/jak/pull/42>`_

* Other:
  * Update the tox.ini file to run tests on Python 3.6 (which we totally support btw.) `(PR#44) <https://github.com/dispel/jak/pull/44>`_
  * Updated copyrights to the year 2017 `(PR#43) <https://github.com/dispel/jak/pull/43>`_


0.14.1
------

Lifecycle: 2016-02-01 - 2017-09-02

* **[0.14.1]** HOTFIX: Import of bytestring compatibility function was removed during a merge, and it happened unnoticed. `(commit) <https://github.com/dispel/jak/commit/582dc724fd24d17dbc16b28debf267640116bd0e>`_

* Other:
   * DOCS: fixed static links for the terminal examples (I guess readthedocs changed something?).


0.14
----

Lifecycle: 2016-02-01 - 2016-02-06

* **[0.14.0]** FEATURE: jak encrypt/decrypt commands can now accept a list of files (jak encrypt file1 ... fileN -k <key>). `(PR#34) <https://github.com/dispel/jak/pull/34>`_
* **[0.13.0]** FEATURE: jak works for all type of files, not just text files. `(PR#33) <https://github.com/dispel/jak/pull/33>`_
* **[0.12.0]** FEATURE: Add encryption versioning. This allows us to upgrade/edit the cipher and still decrypt previous ciphertexts (so they don't become undecryptable) `(PR#31) <https://github.com/dispel/jak/pull/31>`_


0.11
----

Lifecycle: 2017-01-23 - 2017-02-01

* **[0.11.0]** FEATURE: Properly use HMAC to make sure the ciphertext has not been tampered with. `(PR#28) <https://github.com/dispel/jak/pull/28>`_

* Other:
   * Upgraded the dev environment `(PR#29) <https://github.com/dispel/jak/pull/29>`_
   * :ref:`Added security section to the documentation <security>`

Acknowledgements:

* Huge thank you to @obscurerichard (Richard Bullington-McGuire <richard@moduscreate.com> / @obscurerichard on GitHub & Twitter) for figuring out that jaks authentication could be improved.


0.10
----

Lifecycle: ~2017-01.

* **[0.10.0]** FEATURE: Switched to CBC mode for AES from CFB. `(PR#14) <https://github.com/dispel/jak/pull/14>`_
* **[0.10.1]** CLEANUP: Encrypt/Decrypt file services were a mess.. `(PR#15) <https://github.com/dispel/jak/pull/15>`_
* **[0.10.2]** ENHANCEMENT: Make keyfile location in jakfile relative instead of absolute. `(PR#22) <https://github.com/dispel/jak/pull/22>`_
* **[0.10.3]** BUG: Wrong key should print filepath. `(PR#21) <https://github.com/dispel/jak/pull/21>`_
* **[0.10.4]** ENHANCEMENT: Made sure jak worked well in Python 3, 3.3, 3.4 and PyPy. `(PR#19) <https://github.com/dispel/jak/pull/19>`_
* Other:
   * DOCS: Add videos of terminal usage, a ton of text content and this changelog. `(PR#27) <https://github.com/dispel/jak/pull/27>`_


0.0 - 0.9 (Troubled Toddler)
----------------------------

Lifecycle: ~2016-11 - ~2016-12

Birth.

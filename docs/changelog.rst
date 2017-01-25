.. _changelog:


Changelog
=========

1.0 [Not Released Yet] (make way for the Young Whippersnapper)
--------------------------------------------------------------

1.0.0 Will be assigned when we have verified that the encryption is absolutely stable AND
we believe the risk of us accidentally deleting peoples secrets is < 0.0001%. In practice this means better unit testing and talking to 2-3 more cryptography experts (especially outside of Dispel). Are you such an expert? Get in touch! cdilorenzo@dispel.io.


0.14 [soon]
-----------

* **[0.14.0]** `FEATURE: jak encrypt/decrypt commands can now accept a list of files (jak encrypt file1 ... fileN -k <key>). <https://github.com/dispel/jak/pull/34>`_.



0.13 [soon]
-----------

* **[0.13.0]** `FEATURE: jak works for all type of files, not just text files. <https://github.com/dispel/jak/pull/33>`_.


0.12 [soon]
-----------

* **[0.12.0]** `FEATURE: Add encryption versioning. This allows us to upgrade/edit the cipher and still decrypt previous ciphertexts (so they don't become undecryptable) <https://github.com/dispel/jak/pull/31>`_.


0.11 [2017-01-23 - current]
---------------------------

* **[0.11.0]** `FEATURE: Properly use HMAC to make sure the ciphertext has not been tampered with. <https://github.com/dispel/jak/pull/28>`_. Huge thank you to @obscurerichard (Richard Bullington-McGuire <richard@moduscreate.com> / @obscurerichard on GitHub & Twitter) for figuring out that jaks authentication could be vastly improved like this.

* Other:
   * `Upgraded the dev environment <https://github.com/dispel/jak/pull/29>`_


0.10 [~2017-01]
---------------

* **[0.10.0]** `FEATURE: Switched to CBC mode for AES from CFB <https://github.com/dispel/jak/pull/14>`_
* **[0.10.1]** `CLEANUP: Encrypt/Decrypt file services were a mess. <https://github.com/dispel/jak/pull/15>`_
* **[0.10.2]** `ENHANCEMENT: Make keyfile location in jakfile relative instead of absolute <https://github.com/dispel/jak/pull/22>`_
* **[0.10.3]** `BUG: Wrong key should print filepath <https://github.com/dispel/jak/pull/21>`_
* **[0.10.4]** `ENHANCEMENT: Made sure jak worked well in Python 3, 3.3, 3.4 and PyPy <https://github.com/dispel/jak/pull/19>`_
* Other:
   * `DOCS: Add videos of terminal usage, a ton of text content and this changelog. <https://github.com/dispel/jak/pull/27>`_


0.0 - 0.9 [~2016-11 - ~2016-12] (This begins the reign of the Troubled Toddler)
-------------------------------------------------------------------------------

Birth.

.. _security:


Security
========

Read on to get a painstakingly detailed understanding of how secure jak is. If you notice any issues with the security we `encourage you to get in touch, preferably via a github issue. <https://github.com/dispel/jak/issues>`_ or send an email to cdilorenzo@dispel.io.

The source code for the HMAC and cipher is basically in 1 file: https://github.com/dispel/jak/blob/master/jak/aes_cipher.py

Encryption
----------

jak uses the **PyCrypto** implementation of **AES256** running in **CBC-MODE** for it‘s encryption. What makes AES be 256 is the key space of the key you use. For 256-bit you should have a 32 byte key that is as random as possible (more on randomness later). 1 byte is 8 bits so 256 / 8 = 32. This gives you a key space of 2^32. Which is a lot.

jak will requires and will generate a key of the form ``b30259425d7e5a8b4858f72948d7a232142c292997d6431efaa6a02d7a866b03`` which is 64 characters long. To keep it readable we are actually representing the bytes as hexdigits, 2 hex digits are 1 byte of complexity. ``b3 02 59 42`` is 4 bytes. Therefore you might consider the 64 character key as being 32 pairs, meaning bytes. jak generates this key from **/dev/urandom** (``binascii.hexlify(os.urandom(32))``).

For a digression on randomness either scroll down or click here.

CBC-MODE requires padding. jak uses **PKCS#7** padding. In plain English that means that jak pads the secret to be encrypted to a block size of 16 the padding number is equal to the amount of padding. Since showing usually helps for understanding: ``pad('aaaaaaaaaaaaa') returns 'aaaaaaaaaaaaa\x03\x03\x03'``.

CBC-MODE also requires an **Initialization Vector (IV)**. jak generates it using the **Fortuna (PRNG)** as implemented by **PyCrypto**.

Further reading:

* https://www.pycrypto.org
* https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
* https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Block_Chaining_.28CBC.29
* https://en.wikipedia.org/wiki/Key_space_(cryptography)
* https://en.wikipedia.org/wiki/Initialization_vector
* https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS7
* https://en.wikipedia.org/wiki/Fortuna_(PRNG)


HMAC
----

jak uses `Encrypt-then-MAC (EtM) <https://en.wikipedia.org/wiki/Authenticated_encryption>`_ for authenticating. The hash function is **SHA512**.

.. image:: https://upload.wikimedia.org/wikipedia/commons/b/b9/Authenticated_Encryption_EtM.png
   :alt: picture of encrypt then MAC.

Something "funky" that we do is that we use the same key for the HMAC and the AES. The key for the HMAC is simply passed through SHA512, which is questionably necessary. The argument for passing it through SHA512 is basically that it "can‘t hurt" and "better safe than sorry". We would love more expert cryptographers opinions on this.

Further reading:

* https://moxie.org/blog/the-cryptographic-doom-principle/
* https://en.wikipedia.org/wiki/Authenticated_encryption
* https://en.wikipedia.org/wiki/SHA-2


.. _prng_digression:

Obtaining randomness
--------------------

The random things jak generates are the **key** and the **IV**. Measuring randomness is hard if not impossible and there seems to be a great deal of differing opinions about what is a good source. The TL;DR seems to be that /dev/urandom and Fortuna are sufficiently random. But please educate yourself, it's a really interesting subject. Here are some good links to get you started.

* https://docs.python.org/3.5/library/os.html#os.urandom
* https://docs.python.org/2.7/library/os.html#os.urandom
* https://sockpuppet.org/blog/2014/02/25/safely-generate-random-numbers/
* http://www.2uo.de/myths-about-urandom/
* https://github.com/dlitz/pycrypto/blob/master/lib/Crypto/Random/__init__.py


A full example using actual values
----------------------------------

TODO


Final thoughts
--------------

jak has had plenty of skilled eyeballs review it since it's inception. But implementing crypto is a famously hard thing to do and the types of attacks that are available is a continually changing landscape. That is why we encourage as much openness about how jak is implemented as possible so that possible issues can be caught early on.

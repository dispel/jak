.. _security:


Security
========


jak aims to use well-tested computer security methods, including cryptography, to protect your information. What follows is a description of how jak uses cryptographic primitives to achieve this goal. Please report any security issues related to the architecture, design, or implementation you find as a `github issue <https://github.com/dispel/jak/issues>`_ or via email to cdilorenzo@dispel.io

Hopefully this image will be helpful in having you understand how the encryption and authentication works.

.. image:: /_static/jak_crypto_description.jpg
   :alt: flow diagram of how jak encrypts plaintext.


Encryption
----------

jak uses the **PyCryptodome** implementation of **AES256** running in **CBC-MODE** for its encryption. What makes AES be 256 is the key space of the key you use. For 256-bit you should have a 32 byte key that is as random as possible. 1 byte is 8 bits so 256 / 8 = 32. This gives you a key space of 2^32.

jak requires a 64 character hexadecimal key. It can :ref:`generate it for you. <keygen_cmd>`  It should look something like this ``b30259425d7e5a8b4858f72948d7a232142c292997d6431efaa6a02d7a866b03``. To keep it readable we are actually representing the bytes as hexdigits, 2 hex digits are 1 byte of complexity. ``b3 02 59 42`` is 4 bytes. Therefore the 64 character key is 32 bytes. jak generates this key from **/dev/urandom** (``binascii.hexlify(os.urandom(32))``).

CBC-MODE requires padding. jak uses **PKCS#7** padding. In plain English that means that jak pads the plaintext secret to be a multiple of the block size (defaults to 16) by adding padding where each character is a number equal to the amount of padding. The previous sentence might be tricky, so here is an example to clarify: ``pad('aaaaaaaaaaaaa') returns 'aaaaaaaaaaaaa\x03\x03\x03'``.

CBC-MODE also requires an **Initialization Vector (IV)**. jak generates it using the **Fortuna (PRNG)** as implemented by **PyCryptodome**.

Further reading:

* https://pycryptodome.readthedocs.io/en/latest/
* https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
* https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Block_Chaining_.28CBC.29
* https://en.wikipedia.org/wiki/Key_space_(cryptography)
* https://en.wikipedia.org/wiki/Initialization_vector
* `https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS7 <https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS7>`_
* https://en.wikipedia.org/wiki/Fortuna_(PRNG)


HMAC
----

jak uses `Encrypt-then-MAC (EtM) <https://en.wikipedia.org/wiki/Authenticated_encryption>`_ for authentication. The hash function is **SHA512**.

.. image:: https://upload.wikimedia.org/wikipedia/commons/b/b9/Authenticated_Encryption_EtM.png
   :alt: picture of encrypt then MAC.

The key for the HMAC is simply passed through SHA512, which is questionably necessary. The argument for passing it through SHA512 is basically that it "can‘t hurt" and "better safe than sorry". We would love to hear your opinion on this. Read more about our reasoning `here. <http://crypto.stackexchange.com/a/8086>`_

Further reading:

* https://moxie.org/blog/the-cryptographic-doom-principle/
* https://en.wikipedia.org/wiki/Authenticated_encryption
* https://en.wikipedia.org/wiki/SHA-2
* http://crypto.stackexchange.com/a/8086


.. _prng_digression:

Obtaining randomness
--------------------

The random values jak generates are the **key** and the **IV**. Measuring randomness is hard if not impossible and there seems to be a great deal of differing opinions about what is a good source. The TL;DR seems to be that /dev/urandom and Fortuna are sufficiently random. But please educate yourself, it‘s a really interesting subject. Here are some good links to get you started.

* https://docs.python.org/3.9/library/os.html#os.urandom
* https://sockpuppet.org/blog/2014/02/25/safely-generate-random-numbers/
* http://www.2uo.de/myths-about-urandom/


Final thoughts
--------------

Implementing good cryptography has many not-so-subtle opportunities for an implementer, or library, to make a mistake. This situation is not helped by the fact that the types of attacks that are available is a continually changing landscape. That is why we encourage as much openness about how jak is implemented as possible so that possible issues can be caught early on.

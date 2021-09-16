"""
Copyright 2021 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import hmac
import binascii
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from .padding import pad, unpad
from .exceptions import JakException, WrongKeyException


class AES256Cipher:
    """AES256 using CBC mode and a 16bit block size."""

    def __init__(self, key, mode=AES.MODE_CBC):
        """You can override the mode if you want, But you had better know
        what you are doing."""

        self.cipher = AES
        self.mode = mode
        self.BLOCK_SIZE = AES.block_size
        self.SIG_SIZE = SHA512.digest_size
        self.VERSION = 'JAK-000'

        # We force the key to be 64 hexdigits (nibbles) because we are sadists.
        key_issue_exception = JakException(
            "Key must be 64 hexadecimal [0-f] characters long. \n"
             "jak recommends you use the 'keygen' command to generate a strong key.")

        # Long enough?
        if len(key) != 64:
            raise key_issue_exception

        try:
            self.key = binascii.unhexlify(key)
        except (TypeError, binascii.Error):

            # Not all of them are hexadecimals in all likelihood
            raise key_issue_exception

        # Generate a separate HMAC key. This is (to my understanding) not
        # strictly necessary.
        # But was recommended by Thomas Pornin (http://crypto.stackexchange.com/a/8086)
        self.hmac_key = SHA512.new(data=key.encode()).digest()

    def _generate_iv(self):
        """Generates an Initialization Vector (IV).
        https://github.com/Legrandin/pycryptodome/blob/master/lib/Crypto/Random/__init__.py
        Seems to be making use of os.urandom.
        """
        return Random.new().read(self.BLOCK_SIZE)

    def _authenticate(self, data, signature):
        """True if key is correct and data has not been tampered with else False"""
        new_mac = hmac.new(key=self.hmac_key, msg=data, digestmod=SHA512).digest()

        # It is important to compare them like this instead of using '=='
        # to prevent timing attacks
        return hmac.compare_digest(new_mac, signature)

    def extract_iv(self, ciphertext):
        """Extract the IV"""
        return ciphertext[len(self.VERSION):len(self.VERSION) + self.BLOCK_SIZE]

    def _extract_signature(self, ciphertext):
        """extract the HMAC signature"""
        return ciphertext[-self.SIG_SIZE:]

    def _extract_payload(self, ciphertext):
        """Returns the meat and potatoes, the encrypted data payload.
        said another way it doesn't return the IV nor the MAC signature.
        """
        return ciphertext[len(self.VERSION) + self.BLOCK_SIZE:-self.SIG_SIZE]

    def _extract_version(self, ciphertext):
        """Tag the ciphertexts with a version like JAK-001
        that way if we edit the cipher or mac we can still decrypt it but then
        re-encrypt it with the new stronger/bug free encryption.

        >>> self._extract_version('JAK-XXX324872y34g23yug...')
        "JAK-XXX"
        """

        # Could also just write 7 here... just saying.
        return ciphertext[:len('JAK-000')]

    def _need_old_decrypt_function(self, version):
        return version != bytes(self.VERSION, 'utf-8')

    def _use_old_decrypt_function(self, version, ciphertext):
        """jak version is not the current one, so we need to use an old
        decryption function to go back to the plaintext.
        This makes it so we can upgrade the our ciphers and not doom users to
        installing old versions of jak or being unable to decrypt files that
        were generated by previous jak versions."""

        # Haven't upgraded our encryption since we added ciphertext versioning.
        # When we do we will replace this with a switch statement selecting old
        # Decryption methods.
        raise Exception(f'FATAL: No one should end up here.... VERSION: {version}, C: {ciphertext}')

    def decrypt(self, ciphertext):
        """Decrypts a ciphertext secret"""

        # This allows us to upgrade the encryption and MAC
        version = self._extract_version(ciphertext=ciphertext)

        if self._need_old_decrypt_function(version):
            return self._use_old_decrypt_function(
                version=version,
                ciphertext=ciphertext
            )

        signature = self._extract_signature(ciphertext=ciphertext)
        iv = self.extract_iv(ciphertext=ciphertext)
        payload = self._extract_payload(ciphertext=ciphertext)

        if not self._authenticate(data=payload, signature=signature):
            raise WrongKeyException('Wrong key OR the encrypted payload has been tampered with. Either way I am aborting...')  # noqa

        # Setup cipher and perform actual decryption
        cipher_instance = self.cipher.new(key=self.key, mode=self.mode, IV=iv)
        payload_padded = cipher_instance.decrypt(ciphertext=payload)
        return unpad(data=payload_padded)

    def encrypt(self, plaintext, iv=False):
        """Encrypts a plaintext secret"""
        if not iv:
            iv = self._generate_iv()

        cipher_instance = self.cipher.new(key=self.key, mode=self.mode, IV=iv)
        plaintext_padded = pad(data=plaintext)
        encrypted_data = cipher_instance.encrypt(plaintext=plaintext_padded)
        signature = hmac.new(key=self.hmac_key, msg=encrypted_data, digestmod=SHA512).digest()
        return bytes(self.VERSION, 'utf-8') + iv + encrypted_data + signature

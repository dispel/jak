from Crypto.Cipher import AES
from .padding import pad32, PKCS7_16, unPKCS7_16


def encrypt(key, secret):
    """"""
    # if key is not 32 characters pad it.
    # a key with less than 32 characters is really not that secure though...
    # so I wonder if we should actually pad it...
    if len(key) != 32:
        key = pad32(string=key)

    secret = PKCS7_16(unpadded_text=secret)

    # FIXME
    # to IV or not to IV, that is the question.
    # Choose a secure mode.
    # ask someone to validate that what we've done is secure.

    # Debugging
    # print(key)

    aes = AES.new(key=key)
    encrypted_secret = aes.encrypt(secret)
    return encrypted_secret


def decrypt(key, encrypted_secret):
    """"""
    if len(key) != 32:
        key = pad32(string=key)

    aes = AES.new(key=key)
    decrypted_padded_secret = aes.decrypt(encrypted_secret)
    unpadded_secret = unPKCS7_16(padded_text=decrypted_padded_secret)
    return unpadded_secret

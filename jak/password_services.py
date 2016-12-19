# -*- coding: utf-8 -*-

"""
Copyright 2016 Dispel, LLC
Apache 2.0 License, see https://github.com/dispel/jak/blob/master/LICENSE for details.
"""

import os
import binascii


def generate_256bit_key():
    """Generate a secure cryptographically random key."""
    return binascii.hexlify(os.urandom(16))

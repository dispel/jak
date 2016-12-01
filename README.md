# jak

jak is a Troubled Toddler who helps developers encrypt their files.

**OBS!! JAK IS NOT READY FOR PRODUCTION USE YET!!**

# Installation

`pip install jak`

# Usage

```shell

# Create a jakfile (for your settings)
jak init

# You will want to edit the file in a texteditor, it has a
# lot of information in it.
nano jakfile

# Encrypt/Decrypt all of the files that are specified as
# "files_to_encrypt" in your jakfile.
jak encrypt all
jak decrypt all

jak encrypt <specific file>
jak decrypt <specific file>

# Generate a strong password. An encryption is only as strong as the password.
# ALWAYS use a strong 32 character password.
jak genpass

# Where action is one of encrypt/decrypt
# Overrides the password in the jakfile
jak <action> -p 4233afb2bb59fb96ca468511b64a283d

# Overrides the password in the jakfile with a password from a file
jak <action> -pf <password file>
```

# Contributor Guide

See [CONTRIBUTOR_README.md](https://github.com/dispel/jak/blob/master/CONTRIBUTOR_README.md)

# Authors

jak is stewarded and sponsored by [Dispel](https://dispel.io) but all of the contributors are the authors.

# License (gpl-v3)

see [LICENSE](https://github.com/dispel/jak/blob/master/LICENSE) file.

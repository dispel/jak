# jak

jak is a Troubled Toddler who helps developers encrypt their files.

**OBS!! JAK IS NOT READY FOR PRODUCTION USE YET!!**

# Installation

`pip install jak`

# Quickstart

```shell
cd ~/folderThatMayOrMayNotBeARepo
jak start
nano jakfile # add which files you want to have be encrypted.
jak encrypt all
jak decrypt all
```

One off
```shell

# Create a 64 character (32 byte) hex digit (0-f) key.
jak keygen (Optional --minimal)

# Encrypt/Decrypt a specific file
jak encrypt <file> --key <key from keygen command>
jak decrypt <file> --key <key from keygen command>

# If you put the generated key in a file
jak encrypt <file> --keyfile <key file location>
etc.
```

# Usage

```shell
# Initialize jak (if for git repo, stand in it)
jak start

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
jak <action> -p faca44c66af094f18e3e69eaf2328e557a618ca0e3d560a5f83c6f43a172b542

# Overrides the password in the jakfile with a password from a file
jak <action> -pf <password file>

# We highly recommend you read the jak --help man texts.
jak --help

# It works for specific commands as well
jak keygen --help
```

# Contributor Guide

See [CONTRIBUTOR_README.md](https://github.com/dispel/jak/blob/master/CONTRIBUTOR_README.md)

# Authors

jak is stewarded and sponsored by [Dispel](https://dispel.io) but all of the contributors are the authors.

# License (Apache-2.0)

see [LICENSE](https://github.com/dispel/jak/blob/master/LICENSE) file.

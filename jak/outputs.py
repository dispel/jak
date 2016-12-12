FRESH_JAKFILE = u'''// For more information visit https://github.com/dispel/jak/
// Protip: Set your syntax highlighting to JavaScript.
{{
  // RECOMMENDED
  // List files to encrypt here so you can quickly encrypt/decrypt them all
  // using the "$> jak encrypt/decrypt all" commands.

  "files_to_encrypt": ["path/to/file"],

  // I created a secure 32 character key for you. You can make one yourself
  // if you want by using the "$> jak keygen" command.

  "key": "{key}"

  // You can store your key in a file INSTEAD of having a "key" value.
  // This allows you to commit the jakfile. (never commit your key!)
  // "key_file": "path/to/jakkeyfile"
}}'''

KEYGEN_RESPONSE = '''Here is your shiny new key.

{key}

Remember to keep this password secret and save it. Without it you will NOT be able
to decrypt any file(s) you encrypt using it.'''

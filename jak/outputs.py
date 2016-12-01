FRESH_JAKFILE = u'''// For more information visit https://github.com/dispel/jak/
// Protip: Set your syntax highlighting to JavaScript.
{{
  // I created a secure 32 character password for you. You can make one yourself
  // if you want by using the "$> jak genpass" command.

  "password": "{password}",


  // You can store your password in a file INSTEAD of having a "password" value.
  // This allows you to commit the jakfile. (never commit your password!)
  // "password_file": "path/to/jakpasswordfile",


  // RECOMMENDED
  // List files to encrypt here so you can quickly encrypt/decrypt them all
  // using the "$> jak encrypt/decrypt all" commands.

  "files_to_encrypt": ["path/to/file"]
}}'''

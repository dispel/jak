.. _advanced:

Advanced usage
==============

Here we answer questions not many people will have.


Encryption & Security
---------------------

If provided a jak generated key (complexity of the key is what determines the "number" for AES), jak will encrypt the files using AES256 which is secure. Seriously, I cannot stress this enough, using a poor password will result in poor encryption, don't do it! :ref:`Jak will generate the password for you if you ask nicely. <keygen
_cmd>`



.. _jak_folder_adv:

What is in the hidden .jak folder?
----------------------------------

Basically, it holds the things jak doesn't feel like you should need to be looking at.

One of the more important things jak recommends it holds is the :ref:`keyfile <keyfile>` which holds the auto generated key that jak uses.

It also holds the backups used to :ref:`maintain state <maintain_sate>` of the encrypted files.



.. _maintain_state:

How does jak maintain state?
----------------------------

Or stated a different (more verbose) way: **How come the encrypted content of a file doesn't change unless the files content changes?**

jak saves a copy of the encrypted files in the :ref:`.jak folder <jak_folder_adv>` on decryption. On re-encryption it checks whether encrypting the contents with the backups IV creates the same encrypted content. If it is the same it simply reverts to using the previously encrypted content. This method has 2 main benefits: first, it is very simple. If given the option between a simple solution and an advanced one, you should pick the easy one. Two, nothing unencrypted is stored anywhere, the backup is of the encrypted content. The only issue (as described below) is that on encryption you end up performing 2 encryptions instead of 1 for content that has changed, which for very large files (hasn't been measured yet) may incur a time cost that is deemed unacceptable.

The dev team has discussed switching to a slightly more "stupid" way of dealing with this, namely to save the modified time and simply compare that. However that would fail if the file was modified and then the changes were discarded or otherwise changed back. However that would be a constant time lookup, so it may be preferable if we find jak is used for very large files (where performing the encryption twice might become an issue).



How does jak perform the diffing at a merge conflict?
-----------------------------------------------------

Basically jak extracts the LOCAL and REMOTE parts of the merge conflict and decrypts them back into the same file. It then provides some options for a merge tool (or plain for decrypting and then leaving it alone) to merge with.

Example conflict can looks something like this: Where the LOCAL is the top and the REMOTE is the bottom.

.. sourcecode:: plain

   <<<<<<< SOMETHING (usually HEAD)
   <some local like: asfs6e024f69113940ead0
   19e7dc63e7eee99fb5db2ae37352c1d5de8643a3
   f78ae736ae4027fae2acc1530a356dc6d1e360ca
   cyz>
   =======
   <some remote like: asf6e024f69113940ead0
   ff9790b8cccd50e1276c4b9ac18475d4e048f2e0
   4e0034e782b64b1c9e1ac8c1cb81c3b4e43cb93f
   cyz>
   >>>>>>> SOME OTHER HASH

If you are a developer the `code for diffing is right here <https://github.com/dispel/jak/blob/master/jak/diff.py>`_.

[Video of doing diff here?]



How does the pre-commit hook work?
----------------------------------

First and foremost, we recommend against trusting that the pre-commit hook will work, this is a failsafe and should be treated as such.

The pre-commit hook embeds logic into the regular old ``.git/hooks/pre-commit`` hook that exists in all git repositories.
It's functionality in pseudocode is roughly this:

1. Read the jakfile for the list of files that should be encrypted and retreive the key.
2. If it can't get a list of files or there isn't a key, do nothing.
3. If there is a list of files, compare it to the files that are currently staged.
4. If a file is in both the list and in staging, encrypt it.
5. Profit.

To view the actual code you can see it in the `outputs.py <https://github.com/dispel/jak/blob/master/jak/outputs.py>`_ file. It is the ``PRE_COMMIT_ENCRYPT`` variable.

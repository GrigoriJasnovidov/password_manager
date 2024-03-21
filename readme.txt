This simple application allows safely keep passwords for browser using only one master key.

For each website a user should provide alias, url and login. Based on url, login and secret master-key, an 
automatical 64 symbols password is generated using sha256 algorithm. The usage of master-key and hash
functions forces the password to be almost random sequence of numbers and letters a-f. A line containing
alias, url, login and generated password is added to password.gpwd file, while encrypted master-key is saved
in master-key.gpwd file. The cryptography part is based on cryptography and hashlib packages and graphical 
interface relies on CustomTkinter pacakege. 

Buttons:

1. "Exit" - quit application.
2. "Clear" - clear all ouputs frames.
3. "Decrypt passwords" - decrypt and show all passwords. Master-key is neccessary for this operation.
4. "Add Password" - add a new password. Master-key is neccessary for this operation. To add a new password user
                    must fill alias, url and login forms before clicking on this button. The password will be 
                    automatically generated given url and login. The string with alias, url, login and 
                    automatically generated password will be added to passwords.gpwd file. If a password with the
                    same url and login already exists, nothing will be added.
5. "Get Password" - get a password provided url and login. Master-key is neccessary for this operation. The password
                    will be generated automatically for given url and login. 
6. "Remove Last Password" - remove last password. Master-key is neccessary for this operation.
7. "Remove Password" - remove password with given url and login. Master-key is neccessary for this operation.
8. "Show Last Password" - show last password. Master-key is neccessary for this operation.
9. "Change Master-Key" - change master-key. Master-key is necessary for this operation.

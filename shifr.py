from cryptography.fernet import Fernet

from utils import make_formatted_key, check_file_is_empty
from generate_pwd import make_pwd
from verification import check_credentials


class Shifr:
    """Class for auto-generating, cyphering and decrypting password for websites.

    Args:
        key - secret code allowing working with passwords. Must contain only letters or numbers, maximum 43 symbols.
        file_pwds - name of file with passwords
        file_key - name key verification file."""

    def __init__(self,
                 key: str,
                 file_pwds: str,
                 file_key: str,
                 verification_key_string: str):
        """Initialize Shifr object. Initialization is possible only if file agrees with key."""
        self.file_pwds = file_pwds
        self.file_key = file_key
        self.verification_key_string = verification_key_string
        self.key = key
        proceed, mfk = make_formatted_key(key)
        if proceed:
            self.formatted_key = mfk
        else:
            raise ValueError(mfk)
        self.fer = Fernet(self.formatted_key)

        self._bind_file()

    def _bind_file(self):
        """Read file with encrypted master-key and decrypt it with self.key. If succeeds, allows initialization."""

        if check_file_is_empty(file_name=self.file_key):
            encrypted_line = make_verification_key(self.key, string=self.verification_key_string)
            with open(self.file_key, 'w') as f:
                f.write(encrypted_line)
        else:
            with open(self.file_key, 'r') as f:
                encrypted_string = f.read()
                try:
                    self.decrypt_str(encrypted_string)
                except BaseException:
                    raise ValueError('key is not correct. Try authentic code.')

    def encrypt_str(self, string: str):
        """Encrypt a string without '\n'.

        Args:
            string to encrypt."""
        if string == '':
            raise ValueError('String is empty!')
        string = str(string)
        string = bytes(string, encoding='utf')
        return self.fer.encrypt(string).decode()

    def decrypt_str(self, string: str):
        """Decrypt a string without '\n'.

        Args:
            string to decrypt."""
        if string == '':
            raise ValueError('String is empty!')
        string = str(string)
        string = bytes(string, encoding='utf')
        return self.fer.decrypt(string).decode()

    def encrypt_text(self, text: str):
        """Encrypt string with several lines.

        Args:
            text: a string with several lines."""
        if text == '':
            raise ValueError('Text is empty!')
        while text[-1] == '\n':
            text = text[:-1]
        lines = text.split('\n')
        encrypted_text = ''
        for line in lines:
            encrypted_text += self.encrypt_str(line) + '\n'
        return encrypted_text

    def decrypt_text(self, text: str):
        """Decrypt string with several lines.

        Args: text with encrypted strings separated by '\n'."""
        if text == '':
            raise ValueError('Text is empty!')
        while text[-1] == '\n':
            text = text[:-1]
        lines = text.split('\n')
        decrypted_text = ''
        for line in lines:
            decrypted_text += self.decrypt_str(line) + '\n'
        return decrypted_text

    def get_decrypted_pwds(self):
        """Return decrypted passwords."""
        with open(self.file_pwds, 'r') as f:
            content = f.read()

        return self.decrypt_text(text=content)

    def build_pwd(self, alias: str, url: str, login: str):
        """Add a new password to file.

        Args:
            alias - alias
            url - url
            login - login."""
        message = check_credentials(alias=alias, url=url, login=login)
        if message != 'Credentials are correct.':
            raise ValueError(message)
        auto_pwd = make_pwd(url=url, login=login, key=self.formatted_key)
        string = alias + ' ' + url + ' ' + login + ' ' + auto_pwd

        return self.encrypt_str(string)


def make_verification_key(key: str, string: str):
    """For given key returns Fernet(key).encrypt(string).

    Args:
        key - key
        string - some non-secret string to build passwords.
    Returns:
        string encrypted with key."""
    proceed, key = make_formatted_key(key)
    if not proceed:
        raise ValueError(key)
    fer = Fernet(key)
    string = bytes(string, encoding='utf')
    return fer.encrypt(string).decode()


def check_correct_shifr(key: str, file_pwds: str, file_key: str, verification_key_string: str):
    """Try to initialize Shifr-class object given arguments.

    key - key
    file_pwds - file with pwds
    file_key - file with master-key
    verification_key_string.

    Returns:
        Shifr-class object if key and other arguments are correct. Else return False."""
    try:
        return Shifr(key=key, file_pwds=file_pwds, file_key=file_key, verification_key_string=verification_key_string)
    except Exception:
        return False

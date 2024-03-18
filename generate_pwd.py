import hashlib


def make_pwd(url: str,
             login: str,
             key: str):
    """Make password for website.

    The algorithm is following. Sha256 hash of key is concatenated with url and login, and the result is fed to
    sha256 algorithm building password.

    Args:
        url - url
        login - login
        key_generate_pwd - secret code to generate passwords given url; must be memorized and not written anywhere!
    Returns:
        auto-generated password.
    """
    key = bytes(str(key), encoding='utf')
    url = str(url)
    login = str(login)

    hash1 = hashlib.sha256()
    hash1.update(key)
    base_str = hash1.hexdigest()
    pwd_input = bytes(base_str + url + login, encoding='utf')
    hash2 = hashlib.sha256()
    hash2.update(pwd_input)
    pwd = hash2.hexdigest()

    return pwd

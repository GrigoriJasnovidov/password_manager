def check_credentials(alias: str, url: str, login: str):
    """Check correctness of alias, url and login."""

    if len(alias) == 0:
        message = 'Alias must not be empty!'
    elif len(url) == 0:
        message = 'Url must not be empty!'
    elif len(login) == 0:
        message = 'Login must not be empty!'
    else:
        message = 'Credentials are correct.'

    return message

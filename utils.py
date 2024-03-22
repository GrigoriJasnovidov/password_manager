def make_formatted_key(string: str):
    """Make key acceptable for Fernet.

    Args:
        string: a string to covert to password. Must contain letters or numbers, maximum 43 symbols.
    Returns:
        a string fulled up by zeros and '=' at the end. The length of new string is 44 symbols, and it is acceptable for
        Fernet."""
    message = check_key_correctness(string)
    if message == 'Key is correct.':
        string = str(string)
        zeros = '0' * (43 - len(string))
        return True, string + zeros + '='
    else:
        return False, message


def check_key_correctness(string: str):
    string = str(string)
    if not all(x.isspace() or x.isalnum() for x in string):
        return 'Use only numbers and letters for password!'
    elif len(string) > 43:
        return 'Key must be maximum of 43 symbols.'
    else:
        return 'Key is correct.'


def check_file_is_empty(file_name):
    """Check whether file is empty.

    Args:
        file_name - name of the file.
    Returns:
        whether file_name is empty file or not.
    """
    with open(file_name) as f:
        text = f.read()
    return text == ''


def remove_line(text: str, url: str, login: str):
    """Remove line in text with given url and login if exists.

    Args:
        text - text
        url - url
        login - login.
    Returns:
        tuple - (whether a string was found, new text without removed string if exists)."""

    deleted = False
    if text == '':
        raise ValueError('Text is empty!')
    while text[-1] == '\n':
        text = text[:-1]
    lines = text.split('\n')
    for line in lines:
        words = line.split()
        if words[1] == str(url) and words[2] == str(login):
            lines.remove(line)
            deleted = True
            break
    if deleted:
        new_text = ''
        for x in lines:
            new_text += x + '\n'
    else:
        new_text = text
    return deleted, new_text


def get_lines_for_output(text: str):
    """Prepare raw text to be shown in more human-readable format.

    Args:
        text: text to format. Each line must contain exactly alias, url, login and password.
    Returns:
        list of processed lines."""
    if text == '':
        raise ValueError('Text is empty!')
    while text[-1] == '\n':
        text = text[:-1]

    return [f'Alias: {line.split()[0]} url: {line.split()[1]} login: {line.split()[2]} password: {line.split()[3]}'
            for line in text.split('\n')]


def remove_last_line(file_name):
    """Correctly remove last line in a given file.

    Args:
        file_name - name of the file."""

    with open(file_name, 'r') as f:
        lines = f.readlines()
        if lines == []:
            raise ValueError(f'File {file_name} is empty.')
        lines = lines[:-1]
    with open(file_name, 'w') as f:
        f.writelines(lines)


def add_line(file_name, string: str):
    """Correctly add last line.

    Args:
        file_name - name of pwds file
        encrypted string to add."""
    with open(file_name, 'r+') as f:
        f.seek(0, 2)
        f.write(string + '\n')


def approve_adding(text, url, login):
    """Approve whether to add a new password.

    If a line with given url and login already exists in text, then text is unchanged. Otherwise, a line is added.
    Args:
        text - text with already existing passwords, urls, logins, aliases
        url - url
        login - login.
    Returns:
        whether a new line should be added or not."""
    approve = True
    if text == '':
        return approve
    while text[-1] == '\n':
        text = text[:-1]
    lines = text.split('\n')
    for line in lines:
        words = line.split()
        if words[1] == str(url) and words[2] == str(login):
            approve = False
            break
    return approve

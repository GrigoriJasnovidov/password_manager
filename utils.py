def make_formatted_key(string: str):
    """Make key acceptable for Fernet."""
    string = str(string)
    if not all(x.isspace() or x.isalnum() for x in string):
        raise ValueError('Use only numbers and letters for password!')
    elif len(string) > 43:
        raise ValueError('Key must be maximum of 43 symbols.')
    else:
        zeros = '0' * (43 - len(string))
        return string + zeros + '='


def check_file_is_empty(file_name):
    """Check whether file is empty."""
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
        Text without removed string."""

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
        return new_text
    else:
        raise ValueError(f'No line with url={url} and login={login}.')


def get_lines(text: str):
    """Return content of the file in list of lines."""
    if text == '':
        raise ValueError('Text is empty.')
    while text[-1] == '':
        text = text[:-1]
    return text.split('\n')


def get_lines_for_output(text: str):
    if text == '':
        raise ValueError('Text is empty!')
    while text[-1] == '\n':
        text = text[:-1]

    return [f'Alias: {line.split()[0]} url: {line.split()[1]} login: {line.split()[2]} password: {line.split()[3]}'
            for line in text.split('\n')]


def remove_last_line(file_name):
    """Correctly remove last line."""

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
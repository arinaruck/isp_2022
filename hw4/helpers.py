import hashlib


def read_file(path, mode='r'):
    lines = []
    with open(path, mode, errors="ignore") as f:
        for line in f:
            lines.append(line.strip())
    return lines

def check_pass(password, password_hashes, passwords, salt=''):
    m = hashlib.sha256()
    m.update((password + salt).encode())
    hash = m.hexdigest()
    if (hash in password_hashes) and not (password in passwords):
        print(f'Password ({password}) cracked!', flush=True)
        passwords[password] = hash
        return 1
    return 0
from functools import partial
import string
import hashlib
import pickle
from helpers import read_file
from tqdm.auto import tqdm
import multiprocessing
import sys


ALPHABET = string.ascii_lowercase + string.digits
PASSWORD_LENGTH = 8
N_ROWS = 1000000
N_COLS = 5000
TABLE_NAME = 'rainbow'
HASHES_PATH = 'dump_hashes.txt'
N_THREADS = 16
 
def hash_password(password):
    m = hashlib.sha256()
    m.update((password).encode())
    hash = m.hexdigest()
    return hash

def reduce(hash, col):
    d = int(hash, base=16)
    d += col
    base = len(ALPHABET)
    pwd = []
    for _ in range(PASSWORD_LENGTH):
        c_idx = d % base
        pwd.append(ALPHABET[c_idx])
        d = d // base
    return ''.join(pwd)


def create_table_row(row):
    # 8 -- password length
    initial_pwd = f"{row:08d}"
    pwd = initial_pwd
    for col in range(N_COLS):
        hash = hash_password(pwd)
        pwd = reduce(hash, col)
    return hash, initial_pwd
    
def create_table():
    rainbow_table = {}
    pool = multiprocessing.Pool(N_THREADS)
    for r in tqdm(pool.imap_unordered(create_table_row, range(N_ROWS))):
        hash, pwd = r
        rainbow_table[hash] = pwd
    with open(f'{TABLE_NAME}.pickle', 'wb') as handle:
        pickle.dump(rainbow_table, handle, protocol=pickle.HIGHEST_PROTOCOL)


def find_hash(initial_hash, rainbow_table):
    starting_col = N_COLS
    hash = initial_hash
    # finding row
    while hash not in rainbow_table:
        starting_col -= 1
        if starting_col < 0:
            return 0
        hash = initial_hash
        for col in range(starting_col, N_COLS - 1):
            pwd = reduce(hash, col)
            hash = hash_password(pwd)  

    # finding column   
    pwd = rainbow_table[hash]
    for col in range(N_COLS):
        hash = hash_password(pwd)
        if hash == initial_hash:
            print(f'Password ({pwd}) cracked!', flush=True)
            return 1
        pwd = reduce(hash, col)
    return 0
        

def crack_passwords():
    n_hits = 0
    hashes_list = read_file(HASHES_PATH)
    with open(f'{TABLE_NAME}.pickle', 'rb') as handle:
        rainbow_table = pickle.load(handle)
    pool = multiprocessing.Pool(N_THREADS)
    for r in tqdm(pool.imap_unordered(partial(find_hash, rainbow_table=rainbow_table), hashes_list)):
        n_hits += r
    print(f'Success rate: {(n_hits / len(hashes_list)):.5f}')

  
def main(argv):
    if len(argv) != 2:
        raise ValueError(f'Wrong number of arguments ({len(argv)}). Program mode (build_table / crack_passwords) expected')
    if argv[1] == 'build_table':
        create_table()
    elif argv[1] == 'crack_passwords':
        crack_passwords()


if __name__ == '__main__':
    main(sys.argv)
from itertools import product
import string
from tqdm.auto import tqdm
from helpers import check_pass

MIN_LENGTH = 4
MAX_LENGTH = 6
ALPHABET = string.ascii_lowercase + string.digits

password_hashes = [
    '7c58133ee543d78a9fce240ba7a273f37511bfe6835c04e3edf66f308e9bc6e5', 
    '37a2b469df9fc4d31f35f26ddc1168fe03f2361e329d92f4f2ef04af09741fb9',
    '19dbaf86488ec08ba7a824b33571ce427e318d14fc84d3d764bd21ecb29c34ca',
    '06240d77c297bb8bd727d5538a9121039911467c8bb871a935c84a5cfe8291e4', 
    'f5cd3218d18978d6e5ef95dd8c2088b7cde533c217cfef4850dd4b6fa0deef72', 
    'dd9ad1f17965325e4e5de2656152e8a5fce92b1c175947b485833cde0c824d64', 
    '845e7c74bc1b5532fe05a1e682b9781e273498af73f401a099d324fa99121c99', 
    'a6fb7de5b5e11b29bc232c5b5cd3044ca4b70f2cf421dc02b5798a7f68fc0523', 
    '1035f3e1491315d6eaf53f7e9fecf3b81e00139df2720ae361868c609815039c',
    '10dccbaff60f7c6c0217692ad978b52bf036caf81bfcd90bfc9c0552181da85a'
    ]



def main():
    passwords_cracked = 0
    passes = product(ALPHABET,repeat=MIN_LENGTH)
    passwords = {}

    for i, pass_tuple in tqdm(enumerate(passes)):
        password = ''.join(pass_tuple)
        passwords_cracked += check_pass(password, password_hashes, passwords)
        if passwords_cracked == len(password_hashes):
            break
        for c1 in ALPHABET:
            passwords_cracked += check_pass(''.join([password, c1]), password_hashes, passwords)
            if passwords_cracked == len(password_hashes):
                break
            for c2 in ALPHABET:
                passwords_cracked += check_pass(''.join([password, c1, c2]), password_hashes, passwords)
                if passwords_cracked == len(password_hashes):
                    break


if __name__ == '__main__':
    main()
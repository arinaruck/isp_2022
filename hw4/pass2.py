from helpers import read_file, check_pass
import re
from itertools import permutations
from tqdm.auto import tqdm
from pathlib import Path

dict_file = Path('passes_combined.txt')

password_hashes = set([
    '2e41f7133fd134335f566736c03cc02621a03a4d21954c3bec6a1f2807e87b8a',
    '7987d2f5f930524a31e0716314c2710c89ae849b4e51a563be67c82344bcc8da',
    '076f8c265a856303ac6ae57539140e88a3cbce2a2197b872ba6894132ccf92fb',
    'b1ea522fd21e8fe242136488428b8604b83acea430d6fcd36159973f48b1102e',
    '3992b888e772681224099302a5eeb6f8cf27530f7510f0cce1f26e79fdf8ea21', 
    '326e90c0d2e7073d578976d120a4071f83ce6b7bc89c16ecb215d99b3d51a29b',
    '269398301262810bdf542150a2c1b81ffe0e1282856058a0e26bda91512cfdc4', 
    '4fbee71939b9a46db36a3b0feb3d04668692fa020d30909c12b6e00c2d902c31', 
    '55c5a78379afce32da9d633ffe6a7a58fa06f9bbe66ba82af61838be400d624e',
    '5106610b8ac6bc9da787a89bf577e888bce9c07e09e6caaf780d2288c3ec1f0c'
])


def perturb_rule1(password):
    new_password = []
    prev_c = '0'
    for c in password:
        if c.isalpha() and prev_c.isnumeric():
            new_password.append(c.upper())
        else:
            new_password.append(c)
        prev_c = c
    return ''.join(new_password)


def perturb_rule2(password):
    new_password = re.sub('e', '3', password)
    return new_password

def perturb_rule3(password):
    new_password = re.sub('o', '0', password)
    return new_password

def perturb_rule4(password):
    new_password = re.sub('i', '1', password)
    return new_password

rules = [perturb_rule1, perturb_rule2, perturb_rule3, perturb_rule4]


def transform_password(password, rules):
    for rule in rules:
        new_password = rule(password)
    return new_password


def main():
    passwords = {}
    passwords_cracked = 0
    password_dict = read_file(dict_file)
    for password in tqdm(password_dict):
        passwords_cracked += check_pass(password, password_hashes, passwords)
        for k in range(1, len(rules) + 1):
            rule_combs = permutations(rules, r=k)
            for rule_comb in rule_combs:
                password = transform_password(password, rule_comb)
                passwords_cracked += check_pass(password, password_hashes, passwords)
                if passwords_cracked == len(password_hashes):
                    break
    print(passwords)    

if __name__ == '__main__':
    main()
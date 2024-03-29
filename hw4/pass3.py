from helpers import read_file, check_pass
from tqdm.auto import tqdm
from pathlib import Path

dict_file = Path('passes_combined.txt')

password_hashes = ['962642e330bd50792f647c1bf71895c5990be4ebf6b3ca60332befd732aed56c',
                   '8eef79d547f7a6d6a79329be3c7035f8e377f9e629cd9756936ec233969a45a3',
                   'e71067887d50ce854545afdd75d10fa80b841b98bb13272cf4be7ef0619c7dab',
                   '889a22781ef9b72b7689d9982bb3e22d31b6d7cc04db7571178a4496dc5ee128',
                   '6a16f9c6d9542a55c1560c65f25540672db6b6e121a6ba91ee5745dabdc4f208',
                   '2317603823a03507c8d7b2970229ee267d22192b8bb8760bb5fcef2cf4c09edf',
                   'c6c51f8a7319a7d0985babe1b6e4f5c329403d082e05e83d7b9d0bf55876ecdc',
                   'c01304fc36655dd37b5aa8ca96d34382ed9248b87650fffcd6ec70c9342bf451', 
                   'cff39d9be689f0fc7725a43c3bdc7f5be012c840b9db9b547e6e3c454a076fc8', 
                   '662ab7be194cee762494c6d725f29ef6321519035bfb15817e84342829728891'
                ]
salts = ['b9', 'be', 'bc', '72', '9f', '17', '94', '7f', '2e', '24']



def main():
    passwords = {}
    passwords_cracked = 0
    password_dict = read_file(dict_file)
    for password in tqdm(password_dict):
        for i, salt in enumerate(salts): 
            passwords_cracked += check_pass(password, [password_hashes[i]], passwords, salt=salt)
    print(passwords)    

if __name__ == '__main__':
    main()
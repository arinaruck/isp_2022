import requests
import numpy as np
from phe import paillier
import math

api_address = "http://localhost:8000"
PRECISION = 2**(-16)
EXP = -8

TEST_DATA = [0.48555949, 0.29289251, 0.63463107, 0.41933057, 0.78672205, 0.58910837, 0.00739207, 0.31390802, 0.37037496, 0.3375726]
TEST_PRED = 0.44812144746653826

def encrypt_object(datapoint, public_key):
    return [public_key.encrypt(x, precision=PRECISION).ciphertext() for x in datapoint]



def main():
    # create a session
    session = requests.session()
    public_key, private_key = paillier.generate_paillier_keypair()

    for datapoint in [TEST_DATA]:
        encrypted_list = encrypt_object(datapoint, public_key)
        r = session.post(f"{api_address}/prediction", json={"pub_key_n": public_key.n , "enc_feature_vector": encrypted_list}).json()
        encrypted_pred = paillier.EncryptedNumber(public_key, int(r["enc_prediction"]), EXP)
        res = private_key.decrypt(encrypted_pred)
        assert 2**(-16) > abs(res - TEST_PRED), "Prediction is not correct"
        print('All good!')


if __name__ == '__main__':
    main()
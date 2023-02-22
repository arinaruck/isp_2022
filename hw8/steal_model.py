import requests
import numpy as np
from phe import paillier
import math

api_address = "http://localhost:8000"
N_FEATURES = 10
PRECISION = 2**(-16)
EXP = -8

TEST_DATA = [0.48555949, 0.29289251, 0.63463107, 0.41933057, 0.78672205, 0.58910837, 0.00739207, 0.31390802, 0.37037496, 0.3375726]
TEST_PRED = 0.44812144746653826

def encrypt_object(datapoint, public_key):
    return [public_key.encrypt(x, precision=PRECISION).ciphertext() for x in datapoint]


def generate_stealing_data():
    stealing_data = []
    for _ in range(N_FEATURES + 1): 
        stealing_data.append(np.random.uniform(0, 1, N_FEATURES).tolist())
    return stealing_data
    

def discover_model(data, preds):
    N = len(data)
    X = np.ones((N, N_FEATURES + 1))
    X[:, 1:] = np.array(data)
    y = np.array(preds)
    coeffs = np.linalg.solve(X,y)
    bias = coeffs[0]
    weights = coeffs[1:]
    return weights, bias


def main():
    # create a session
    session = requests.session()
    public_key, private_key = paillier.generate_paillier_keypair()

    stealing_data = generate_stealing_data()
    preds = []
    for _, datapoint in enumerate(stealing_data):
        encrypted_list = encrypt_object(datapoint, public_key)
        r = session.post(f"{api_address}/prediction", json={"pub_key_n": public_key.n , "enc_feature_vector": encrypted_list}).json()
        encrypted_pred = paillier.EncryptedNumber(public_key, int(r["enc_prediction"]), EXP)
        res = private_key.decrypt(encrypted_pred)
        preds.append(res)
    weights, bias = discover_model(stealing_data, preds)
    print(f'weights:\n{weights}')
    print(f'bias: {bias:.3f}')

    stolen_pred = np.dot(TEST_DATA, weights) + bias
    assert 2**(-16) > abs(stolen_pred - TEST_PRED), "Prediction is not correct"
    print('All good!')



if __name__ == '__main__':
    main()
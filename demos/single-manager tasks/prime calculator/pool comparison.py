import multiprocessing
import multiprocessing as mp
import time

"""
This demonstrates that you can directly use the Manager for single tasks that are intensive with very little code
"""


def is_prime(n):
    for number in range(2, n):
        if (n % number) == 0:
            return False
    return True


if __name__ == "__main__":
    mp.freeze_support()

    start = time.time()
    with multiprocessing.Pool(processes=8) as pool:
        _ = pool.map(is_prime, [i for i in range(200_000)])

    print("8 processes:", time.time() - start)

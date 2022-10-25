import multiprocessing
import multiprocessing as mp
import time
import math

"""
This demonstrates that you can directly use the Manager for single tasks that are intensive with very little code
"""


def get_factorial(n):
    return math.factorial(n)

if __name__ == "__main__":
    mp.freeze_support()

    start = time.time()
    with multiprocessing.Pool(processes=8) as pool:
        _ = pool.map(get_factorial, [i for i in range(50_000)])

    print("8 processes:", time.time() - start)

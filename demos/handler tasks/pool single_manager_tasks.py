import math
import multiprocessing as mp
import time
import src.Manager as Ma
import src.Handler as Ha


def get_factorial(n):
    return math.factorial(n)


def is_prime(n):
    for number in range(2, n):
        if (n % number) == 0:
            return False
    return True


if __name__ == "__main__":
    mp.freeze_support()

    data = [i for i in range(50_000)]

    start = time.time()
    with mp.Pool(processes=8) as p:
        _ = p.map(is_prime, data)

    with mp.Pool(processes=8) as p:
        _2 = p.map(get_factorial, data)
    print(time.time() - start, "s")

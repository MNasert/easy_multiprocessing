import time
import math


def get_factorial(n):
    return math.factorial(n)


if __name__ == "__main__":
    res = []
    start = time.time()
    for i in range(50_000):
        res.append(get_factorial(i))
    print("Single process:", time.time() - start)

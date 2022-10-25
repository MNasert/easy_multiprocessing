import time


def is_prime(n):
    for number in range(2, n):
        if (n % number) == 0:
            return False
    return True


if __name__ == "__main__":
    res = []
    start = time.time()
    for i in range(200_000):
        res.append(is_prime(i))
    print("Single process:", time.time() - start)

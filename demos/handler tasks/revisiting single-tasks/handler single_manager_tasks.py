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

    Manager_prime = Ma.WorkerManager(
        task=is_prime,
        data=data,
        requirements=None,
        data_keys=None,
        desired_num_workers=8
    )

    Manager_fac = Ma.WorkerManager(
        task=get_factorial,
        data=data,
        requirements=[is_prime],
        data_keys=None,
        desired_num_workers=8
    )

    start = time.time()
    Handler = Ha.ProcessHandler([Manager_fac, Manager_prime],
                                limit_processes=8)
    results = Handler.start()
    print(time.time() - start, "s")

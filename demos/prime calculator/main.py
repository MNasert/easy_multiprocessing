import src.Manager as Ma
import multiprocessing as mp
import time


def is_prime(n):
    for number in range(2, n):
        if (n % number) == 0:
            return False
    return True


if __name__ == "__main__":
    res = []
    start = time.time()
    for i in range(100000):
        res.append(is_prime(i))
    print("Single process:", time.time() - start)

    mp.freeze_support()

    start = time.time()
    manager = Ma.WorkerManager(
        task=is_prime,
        data=[i for i in range(100000)],
        desired_num_workers=10,
        requirements=None,
    )
    manager.generate_worker(8)
    manager.start()
    print("8 processes:", time.time() - start)
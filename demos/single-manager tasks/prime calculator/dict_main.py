import src.Manager as Ma
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

    data_dict = {}

    for i in range(500_000):
        data_dict[str(i)] = i

    start = time.time()
    manager = Ma.WorkerManager(
        task=is_prime,
        data=data_dict,
        desired_num_workers=8,
        requirements=None,
        data_keys=data_dict.keys()  # choose your target layer and then go!
    )
    manager.generate_workers(8)
    manager.start_single()
    print("8 processes:", time.time() - start)

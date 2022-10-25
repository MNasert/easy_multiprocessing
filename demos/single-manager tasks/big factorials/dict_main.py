import src.Manager as Ma
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

    data_dict = {}

    for i in range(50_000):
        data_dict[str(i)] = i

    start = time.time()
    manager = Ma.WorkerManager(
        task=get_factorial,
        data=data_dict,
        desired_num_workers=8,
        requirements=None,
        data_keys=data_dict.keys()
    )
    manager.generate_worker(8)
    manager.start()
    print("8 processes:", time.time() - start)

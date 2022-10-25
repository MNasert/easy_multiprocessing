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
    start = time.time()
    manager = Ma.WorkerManager(
        task=get_factorial,
        data=[i for i in range(50_000)],
        desired_num_workers=8,
        requirements=None,
    )
    manager.generate_worker(8)
    manager.start()
    print("8 processes:", time.time() - start)

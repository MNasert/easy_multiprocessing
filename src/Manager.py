from collections.abc import Callable
from typing import List
import multiprocessing as mp

from src.Worker import WorkerInstance
import src.tools.Signals as Signals


class WorkerManager:
    def __init__(self,        # i    o
                 task: Callable,
                 data: dict or list,  # last layer _must_ be list
                 desired_num_workers: int,
                 requirements: List[Callable] = None,  # what methods must be done already (if necessary)
                 data_keys: list = None,  # Only needed if data is dict
                 poll_timeout: float = .1  # timeout for polling each worker; in ms
                 ):

        self.task = task
        self.data = data

        self.desired_num_workers = desired_num_workers
        self.requirements = requirements
        self.data_keys = data_keys

        self.__workers__: List[WorkerInstance] = []  # typehint for IDE and reader
        self.__iterator__ = self.data_iterator()
        self.__poll_timeout__ = poll_timeout * (1/1000)
        self.__index_memory__ = {}
        self.__active_workers__ = 0
        self.results = {}

    def data_iterator(self):
        counter = -1
        if self.data_keys:
            endlevel = self.data
            for key in self.data_keys:
                endlevel = endlevel[key]
            while counter < len(endlevel) - 1:
                res = self.data
                counter += 1
                for layer in self.data_keys:
                    res = res[layer]
                yield res[counter]
            while True:
                yield Signals.__ExitSignal__
        else:
            while counter < len(self.data) - 1:
                counter += 1
                yield self.data[counter]
            while True:
                yield Signals.__ExitSignal__

    def generate_worker(self, num_processes: int) -> None:
        for worker in range(num_processes):

            connection_worker, connection_manager = mp.Pipe()
            self.__index_memory__[worker] = 0 + len(self.__workers__)
            self.__active_workers__ += 1
            self.__workers__.append(

                WorkerInstance(
                    method=self.task,
                    connection_worker=connection_worker,
                    connection_manager=connection_manager,
                    worker_id=worker
                )
            )

    def start(self) -> object:
        for worker in self.__workers__:
            worker.start()

        working = True
        while working:
            working = False
            for worker in self.__workers__:
                if worker.is_alive:
                    self.check_worker(worker)
                    working = True

        return self.results

    def check_worker(self, worker: WorkerInstance) -> None:
        if worker.poll(self.__poll_timeout__):
            key, result = worker.get()
            self.results[key] = result
            data = next(self.__iterator__)
            worker.set(data)
            if data == Signals.__ExitSignal__:
                worker.kill()

        if worker.needs_work:
            data = next(self.__iterator__)
            worker.set(data)


from collections.abc import Callable
from typing import List, Union, KeysView
import multiprocessing as mp

from src.Worker import WorkerInstance
import src.tools.Signals as Signals


class WorkerManager:
    def __init__(self,        # i    o
                 task: Callable,
                 data: dict or list,  # last layer _must_ be list
                 desired_num_workers: int,
                 requirements: List[Callable] = None,  # what methods must be done already (if necessary)
                 data_keys: Union[KeysView, List] = None,  # Only needed if data is dict
                 poll_timeout: float = .01,  # timeout for polling each worker; in ms
                 logging: bool = False):

        self.task = task
        self.data = data

        self.desired_num_workers = desired_num_workers
        self.requirements = [hash(requirement) for requirement in requirements] if requirements else []
        self.data_keys = data_keys  # FIXME: if I want to put output of previous manager as input?
                                    # -> fixed -> KeysView gets updated with dict update -> include in demo

        self.logging = logging
        self.results = {}

        self.__workers: List[WorkerInstance] = []  # typehint for IDE and reader
        self.__iterator = self.data_iterator()
        self.__poll_timeout = poll_timeout * (1 / 1000)
        self.__active_workers = 0

    def data_iterator(self):
        if self.data_keys:
            for key in self.data_keys:
                yield self.data[key]
            while True:
                yield Signals.__ExitSignal__
        else:
            for data_point in self.data:
                yield data_point
            while True:
                yield Signals.__ExitSignal__

    def generate_workers(self, num_processes: int) -> None:
        for worker in range(num_processes):

            connection_worker, connection_manager = mp.Pipe()
            self.__active_workers += 1
            self.__workers.append(

                WorkerInstance(
                    method=self.task,
                    connection_worker=connection_worker,
                    connection_manager=connection_manager,
                    worker_id=worker
                )
            )

        if self.logging:
            print(str(self) + ": started", len(self.__workers), "processes")

    def start(self) -> None:
        for worker in self.__workers:
            worker.start()

    def start_single(self) -> None:
        for worker in self.__workers:
            worker.start()

        working = True
        while working:
            working = self.check_workers()

    def check_worker(self, worker: WorkerInstance) -> bool:
        if worker.poll(self.__poll_timeout):
            key, result = worker.get()
            self.results[key] = result
            data = next(self.__iterator)
            worker.set(data)
            if data == Signals.__ExitSignal__:
                worker.kill()

        if worker.needs_work:
            data = next(self.__iterator)
            worker.set(data)

        return worker.is_alive

    def check_workers(self) -> bool:
        working = False
        for worker in self.__workers:
            self.check_worker(worker)
            if worker.is_alive:
                working = True
        return working

    def __hash__(self) -> int:
        return sum(self.requirements) + hash(self.task)

    def __str__(self) -> str:
        return self.task.__qualname__ + " Manager"

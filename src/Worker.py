from collections.abc import Callable
from typing import Tuple
import multiprocessing as mp
import src.tools.Signals as Signals
import multiprocessing.connection as connection


class WorkerInstance:
    def __init__(self,
                 method: Callable,
                 connection_worker: connection,
                 connection_manager: connection,
                 worker_id: int,  # identifier
                 *args,
                 **kwargs):
        self.method = method
        self.connection_worker = connection_worker
        self.connection_manager = connection_manager
        self.id = worker_id

        self.__process = mp.Process(target=self.worker_start, args=(self.method,
                                                                    connection_worker))
        self.is_alive = False
        self.needs_work = True

    @staticmethod
    def worker_start(method, connection_worker) -> None:
        while True:
            data = connection_worker.recv()

            if data == Signals.__ExitSignal__:
                connection_worker.close()
            result = method(data)
            connection_worker.send((data, result))

    def __kill(self) -> None:
        self.connection_manager.send(Signals.__ExitSignal__)
        self.__process.terminate()

    def start(self) -> None:
        self.is_alive = True
        self.__process.start()

    def kill(self) -> None:
        self.is_alive = False
        self.__kill()

    def get(self) -> Tuple:
        return self.connection_manager.recv()

    def set(self, data) -> None:
        self.connection_manager.send(data)
        self.needs_work = False

    def poll(self, timeout) -> bool:
        if self.connection_manager.poll(timeout):
            self.needs_work = True
            return True
        return False

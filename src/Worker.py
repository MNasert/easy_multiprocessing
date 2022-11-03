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
        self.is_alive = False
        self.needs_work = True

        self.__process = mp.Process(target=self.__start__, args=(self.method,
                                                                 connection_worker))


    @staticmethod
    def __start__(method: Callable, connection_worker: connection) -> None:
        while True:
            data = connection_worker.recv()

            if data == Signals.EXIT_SIGNAL:
                connection_worker.close()
            result = method(data)
            connection_worker.send((data, result))

    def __kill(self) -> None:
        self.connection_manager.send(Signals.EXIT_SIGNAL)
        self.__process.terminate()

    def start(self) -> None:
        self.is_alive = True
        self.__process.start()

    def kill(self) -> None:
        self.is_alive = False
        self.__kill()

    def get(self) -> Tuple:
        return self.connection_manager.recv()

    def set(self, data: object) -> None:
        self.connection_manager.send(data)
        self.needs_work = False

    def poll(self, timeout: float) -> bool:
        if self.connection_manager.poll(timeout):
            self.needs_work = True
            return True
        return False

from collections.abc import Callable
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

        self.__process__ = mp.Process(target=self.__start__, args=(self.method,
                                                                   connection_worker))
        self.is_alive = False
        self.needs_work = True

    @staticmethod
    def __start__(method, connection_worker):
        while True:
            data = connection_worker.recv()

            if data == Signals.__ExitSignal__:
                connection_worker.close()
            result = method(data)
            connection_worker.send((data, result))

    def __kill__(self):
        self.connection_manager.send(Signals.__ExitSignal__)
        self.__process__.terminate()

    def start(self):
        self.is_alive = True
        self.__process__.start()

    def kill(self):
        self.is_alive = False
        self.__kill__()

    def get(self):
        return self.connection_manager.recv()

    def set(self, data):
        self.connection_manager.send(data)
        self.needs_work = False

    def poll(self, timeout) -> bool:
        if self.connection_manager.poll(timeout):
            self.needs_work = True
            return True
        return False

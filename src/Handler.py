import psutil
from typing import List, Tuple
from src.Manager import WorkerManager
import src.tools.Signals as Signals


class ProcessHandler:
    def __init__(self,
                 managers: List[WorkerManager],
                 maxram: float = -1,
                 logging=False):
        self.managers = managers
        self.maxram = maxram
        self.logging = logging
        self.__fullfilled_tasks = []

    def start(self):
        raise NotImplementedError

    def is_alive(self):
        raise NotImplementedError

    def kill(self):
        raise NotImplementedError

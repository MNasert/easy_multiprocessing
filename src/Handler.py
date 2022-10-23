from typing import List, Tuple
from Manager import WorkerManager


class ProcessHandler:
    # constants

    def __init__(self,
                 managers: List[WorkerManager],
                 maxram: float = -1,
                 logging=False):
        self.managers = managers
        self.maxram = maxram
        self.logging = logging

    def start(self):
        raise NotImplementedError

    def is_alive(self):
        raise NotImplementedError

    def kill(self):
        raise NotImplementedError

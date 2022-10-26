import psutil
from typing import List, Tuple
from src.Manager import WorkerManager
import src.tools.Signals as Signals


class ProcessHandler:
    def __init__(self,
                 managers: List[WorkerManager],
                 maxram: float = -1,
                 limit_processes: int = -1,
                 logging: bool = False):
        self.managers = managers
        self.maxram = maxram
        self.logging = logging

        self.__sum_desired_procs = 0
        self.__managerlist = []
        self.__max_processes = psutil.cpu_count(logical=False) if limit_processes == -1 else limit_processes
        self.__scheduled_managers = []
        self.__results = {}
        self.__fullfilled_tasks = []

    def start(self) -> dict:
        done = False
        while not done:
            self.__managerlist = []
            self.order_managers()
            for manager in self.__scheduled_managers:
                manager.generate_workers(max(int(manager.desired_num_workers*(manager.desired_num_workers/self.__sum_desired_procs)), self.__max_processes))
                manager.start()
                if self.logging:
                    print("MAIN:", str(manager), "started")
                self.__managerlist.append(manager)

            working = True
            while working:
                working = self.watch_managers()

            for manager in self.__managerlist:
                self.__fullfilled_tasks.append(hash(manager))
                self.__results[hash(manager)] = manager.results
                if self.logging:
                    print("MAIN:", str(manager), "finished")
                    print("MAIN: results of", str(manager), "put in", hash(manager))

            done = (sum(self.__fullfilled_tasks) == sum([hash(i) for i in self.managers]))

        return self.__results

    def watch_managers(self) -> bool:
        working = False
        for manager in self.__managerlist:
            if manager.check_workers():
                working = True
        return working

    def order_managers(self):
        self.__scheduled_managers = []
        self.__sum_desired_procs = 0
        for manager in self.managers:
            if self.logging:
                manager.logging = self.logging
            if self.__fullfilled_tasks == manager.requirements and hash(manager) not in self.__fullfilled_tasks:
                self.__scheduled_managers.append(manager)

        for manager in self.__scheduled_managers:
            self.__sum_desired_procs += manager.desired_num_workers

    def is_alive(self):
        raise NotImplementedError

    def kill(self):
        raise NotImplementedError

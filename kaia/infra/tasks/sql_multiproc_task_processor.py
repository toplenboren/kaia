from typing import *
from .sql_task_processor import SqlTaskProcessor
import atexit
import os
from ..sql_messenger import SqlMessenger
from ..loc import Loc
from .task_cycle import TaskCycle
from uuid import uuid4
import multiprocessing

class SqlMultiprocTaskProcessor(SqlTaskProcessor):
    def __init__(self, task_cycle: TaskCycle, suffix = None):
        if suffix is None:
            suffix = str(uuid4())
        path = Loc.temp_folder/f'signalling_db/{suffix}'
        os.makedirs(path.parent, exist_ok=True)
        messenger = SqlMessenger(path)
        super(SqlMultiprocTaskProcessor, self).__init__(messenger)
        self.task_cycle = task_cycle
        self.process = multiprocessing.Process(target=task_cycle.run, args=(self.messenger,))

    def activate(self):
        atexit.register(self.deactivate)
        self.process.start()

    def deactivate(self):
        if self.process.is_alive():
            self.process.terminate()

from __future__ import annotations

from typing import TYPE_CHECKING

from utils.core import Core
from utils.visualizer import visualize

if TYPE_CHECKING:
    from utils.scheduler import Scheduler
    from utils.task import Task


class Processor:
    def __init__(
        self, name: str, core_count: int, scheduler: Scheduler, simulation_time: int
    ):
        self.name: str = name

        self.simulation_time: int = simulation_time

        self.scheduler: Scheduler = scheduler
        self.scheduler.set_processor(self)

        self.cores: list[Core] = []
        self.initialize_cores(core_count)

        self.tasks: list[Task] = []

        self.time: int = 0

    def initialize_cores(self, count: int):
        if len(self.cores) == 0:
            for i in range(count):
                self.cores.append(Core(i, self))

    def add_tasks(self, *tasks: Task):
        for task in tasks:
            task.set_processor(self)
            self.tasks.append(task)

    def tick(self):
        self.time += 1

    def start(self):
        self.scheduler.initialize()
        while self.time <= self.simulation_time:
            self.scheduler.schedule()
            for core in self.cores:
                core.process()
            self.tick()
        visualize(self.name, self.cores, self.simulation_time)

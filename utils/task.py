from __future__ import annotations

from typing import TYPE_CHECKING

from utils.job import Job

if TYPE_CHECKING:
    from utils.processor import Processor


class Task:
    def __init__(
        self,
        name: str,
        period: int,
        deadline: int,
        execution_time: int,
    ):
        self.name = name

        self.period = period
        self.execution_time = execution_time
        self.deadline = deadline

        self.active_job = None

        self.last_iteration = -1
        self.last_iteration_time = -1

    @property
    def is_running(self):
        if self.active_job is None:
            return False
        return self.active_job.is_running

    def set_priority(self, priority: int):
        self.priority: int = priority

    def set_processor(self, processor: Processor):
        self.proc = processor

    def create_job(self):
        self.active_job = Job(self, self.last_iteration + 1)
        self.last_iteration_time = self.proc.time
        self.last_iteration += 1
        return self.active_job

from __future__ import annotations

from typing import TYPE_CHECKING

from utils.record import Record

if TYPE_CHECKING:
    from utils.core import Core
    from utils.task import Task


class Job:
    def __init__(self, task: Task, id: int):
        self.id: int = id

        self.task: Task = task

        self.release_time: int = self.task.proc.time

        self.start_time: int = -1
        self.finish_time: int = -1

        self.is_running: bool = False

        self.ut = 0

        self.resume_time = -1

    @property
    def used_time(self):
        return self.ut + (self.task.proc.time - self.resume_time)

    @property
    def remaining_time(self):
        return self.task.execution_time - self.used_time

    @property
    def execution_time(self):
        return self.task.execution_time

    @property
    def period(self):
        return self.task.period

    @property
    def relative_deadline(self):
        return self.task.deadline

    @property
    def absolute_deadline(self):
        return self.release_time + self.task.deadline

    @property
    def laxity(self):
        return self.absolute_deadline - self.remaining_time - self.task.proc.time

    @property
    def is_done(self):
        return self.used_time == self.task.execution_time

    def finalize(self):
        self.finish_time = self.task.proc.time

    def run(self):
        # print(
        #     f"running task {self.task.name} at iteration {self.id} at time {self.task.proc.time}"
        # )

        if not self.is_running:
            self.is_running = True
            self.resume_time = self.task.proc.time

        if self.start_time == -1:
            self.start_time = self.task.proc.time

        self.last_time_stamp = self.task.proc.time

    def halt(self, core: Core):
        if self.is_running:
            self.is_running = False
            self.ut += self.task.proc.time - self.resume_time
            core.history.append(Record(self, self.resume_time, self.task.proc.time))

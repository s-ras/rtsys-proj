from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.job import Job


class Record:
    def __init__(self, job: Job, resumption_time: int, preemption_time: int):
        self.job = job
        self.record_priority = job.task.priority
        self.resumption_time = resumption_time
        self.preemption_time = preemption_time

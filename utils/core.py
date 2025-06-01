from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.job import Job
    from utils.processor import Processor
    from utils.record import Record


class Core:
    def __init__(self, id: int, processor: Processor):
        self.id: int = id

        self.active_job: Job | None = None

        self.proc = processor

        self.history: list[Record] = []

    @property
    def is_free(self):
        return self.active_job is None

    def set_current_job(self, job: Job):
        if self.active_job is not None:
            self.remove_current_job()
        self.active_job = job

    def remove_current_job(self):
        if self.active_job is not None:
            j = self.active_job
            j.halt(self)
            self.active_job = None
            return j

    def process(self):
        if self.active_job is not None:
            self.active_job.run()

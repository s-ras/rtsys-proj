from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.job import Job
    from utils.processor import Processor


class Scheduler:
    def __init__(self):
        pass

    @property
    def time(self):
        return self.proc.time

    @property
    def tasks(self):
        return self.proc.tasks

    def set_processor(self, processor: Processor):
        self.proc = processor

    def handle_finished_jobs(self):
        for core in self.proc.cores:
            if core.active_job is not None and core.active_job.is_done:
                core.active_job.finalize()
                core.remove_current_job()

    def schedule(self):
        pass

    def initialize(self):
        pass


class RM(Scheduler):
    def __init__(self):
        self.ready_list: set[Job] = set()

    def initialize(self):
        self.proc.tasks.sort(key=lambda task: task.period)
        for i, task in enumerate(self.proc.tasks):
            task.set_priority(i + 1)
            self.ready_list.add(task.create_job())

    def iterate_jobs(self):
        for task in self.proc.tasks:
            if self.proc.time - task.last_iteration_time >= task.period:
                self.ready_list.add(task.create_job())

    def schedule(self):
        self.iterate_jobs()
        self.handle_finished_jobs()

        if len(self.ready_list) > 0:
            candidate_job = min(self.ready_list, key=lambda job: job.task.priority)

            candidate_core = min(
                self.proc.cores,
                key=lambda core: (
                    0 if core.is_free else 1,
                    core.active_job.task.priority if core.active_job else 0,
                ),
            )

            if candidate_core.active_job is None:
                candidate_core.set_current_job(candidate_job)
                self.ready_list.remove(candidate_job)
            else:
                if (
                    candidate_core.active_job.task.priority
                    > candidate_job.task.priority
                ):
                    # print(
                    #     f"PREEMPTING {candidate_core.active_job.task.name} with priority {candidate_core.active_job.task.priority} in favor of {candidate_job.task.name} with priority {candidate_job.task.priority}"
                    # )
                    self.ready_list.add(candidate_core.remove_current_job())  # type: ignore
                    candidate_core.set_current_job(candidate_job)
                    self.ready_list.remove(candidate_job)


class DM(Scheduler):
    def __init__(self):
        self.ready_list: set[Job] = set()

    def initialize(self):
        self.proc.tasks.sort(key=lambda task: task.deadline)
        for i, task in enumerate(self.proc.tasks):
            task.set_priority(i + 1)
            self.ready_list.add(task.create_job())

    def iterate_jobs(self):
        for task in self.proc.tasks:
            if self.proc.time - task.last_iteration_time >= task.period:
                self.ready_list.add(task.create_job())

    def schedule(self):
        self.iterate_jobs()
        self.handle_finished_jobs()

        if len(self.ready_list) > 0:
            candidate_job = min(self.ready_list, key=lambda job: job.task.priority)

            candidate_core = min(
                self.proc.cores,
                key=lambda core: (
                    0 if core.is_free else 1,
                    core.active_job.task.priority if core.active_job else 0,
                ),
            )

            if candidate_core.active_job is None:
                candidate_core.set_current_job(candidate_job)
                self.ready_list.remove(candidate_job)
            else:
                if (
                    candidate_core.active_job.task.priority
                    > candidate_job.task.priority
                ):
                    # print(
                    #     f"PREEMPTING {candidate_core.active_job.task.name} with priority {candidate_core.active_job.task.priority} in favor of {candidate_job.task.name} with priority {candidate_job.task.priority}"
                    # )
                    self.ready_list.add(candidate_core.remove_current_job())  # type: ignore
                    candidate_core.set_current_job(candidate_job)
                    self.ready_list.remove(candidate_job)


class EDF(Scheduler):
    def __init__(self):
        self.ready_list: list[Job] = []

    def initialize(self):
        self.proc.tasks.sort(key=lambda task: task.deadline)
        for i, task in enumerate(self.proc.tasks):
            task.set_priority(i + 1)
            self.ready_list.append(task.create_job())

    def prioritize(self):
        self.ready_list.sort(key=lambda job: job.absolute_deadline)
        for i, job in enumerate(self.ready_list):
            job.task.set_priority(i + 1)

    def iterate_jobs(self):
        for task in self.proc.tasks:
            if self.proc.time - task.last_iteration_time >= task.period:
                self.ready_list.append(task.create_job())

    def schedule(self):
        self.iterate_jobs()
        self.handle_finished_jobs()
        self.prioritize()

        if len(self.ready_list) > 0:
            candidate_job = min(self.ready_list, key=lambda job: job.task.priority)

            candidate_core = min(
                self.proc.cores,
                key=lambda core: (
                    0 if core.is_free else 1,
                    core.active_job.task.priority if core.active_job else 0,
                ),
            )

            if candidate_core.active_job is None:
                candidate_core.set_current_job(candidate_job)
                self.ready_list.remove(candidate_job)
            else:
                if (
                    candidate_core.active_job.task.priority
                    > candidate_job.task.priority
                ):
                    # print(
                    #     f"PREEMPTING {candidate_core.active_job.task.name} with priority {candidate_core.active_job.task.priority} in favor of {candidate_job.task.name} with priority {candidate_job.task.priority}"
                    # )
                    self.ready_list.append(candidate_core.remove_current_job())  # type: ignore
                    candidate_core.set_current_job(candidate_job)
                    self.ready_list.remove(candidate_job)


class LLF(Scheduler):
    def __init__(self):
        self.ready_list: list[Job] = []

    def initialize(self):
        for task in self.proc.tasks:
            self.ready_list.append(task.create_job())

        self.ready_list.sort(key=lambda job: job.laxity)

        for i, job in enumerate(self.ready_list):
            job.task.set_priority(i + 1)

    def prioritize(self):
        self.ready_list.sort(key=lambda job: job.laxity)
        for i, job in enumerate(self.ready_list):
            job.task.set_priority(i + 1)

    def iterate_jobs(self):
        for task in self.proc.tasks:
            if self.proc.time - task.last_iteration_time >= task.period:
                self.ready_list.append(task.create_job())

    def schedule(self):
        self.iterate_jobs()
        self.handle_finished_jobs()
        self.prioritize()

        if len(self.ready_list) > 0:
            candidate_job = min(self.ready_list, key=lambda job: job.task.priority)

            candidate_core = min(
                self.proc.cores,
                key=lambda core: (
                    0 if core.is_free else 1,
                    core.active_job.task.priority if core.active_job else 0,
                ),
            )

            if candidate_core.active_job is None:
                candidate_core.set_current_job(candidate_job)
                self.ready_list.remove(candidate_job)
            else:
                if (
                    candidate_core.active_job.task.priority
                    > candidate_job.task.priority
                ):
                    # print(
                    #     f"PREEMPTING {candidate_core.active_job.task.name} with priority {candidate_core.active_job.task.priority} in favor of {candidate_job.task.name} with priority {candidate_job.task.priority}"
                    # )
                    self.ready_list.append(candidate_core.remove_current_job())  # type: ignore
                    candidate_core.set_current_job(candidate_job)
                    self.ready_list.remove(candidate_job)

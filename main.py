from utils.processor import Processor
from utils.scheduler import DM, EDF, LLF, RM
from utils.task import Task


def main():
    p1 = Processor("Rate Monotonic", 4, RM(), 100)
    p1.add_tasks(
        Task(name="T1", period=20, deadline=7, execution_time=3),
        Task(name="T2", period=5, deadline=4, execution_time=2),
        Task(name="T3", period=10, deadline=8, execution_time=1),
        Task(name="T4", period=25, deadline=12, execution_time=3),
    )
    p2 = Processor("Deadline Monotonic", 4, DM(), 100)
    p2.add_tasks(
        Task(name="T1", period=20, deadline=10, execution_time=3),
        Task(name="T2", period=15, deadline=7, execution_time=2),
        Task(name="T3", period=10, deadline=9, execution_time=1),
        Task(name="T4", period=25, deadline=12, execution_time=3),
    )
    p3 = Processor("Earliest Deadline First", 4, EDF(), 100)
    p3.add_tasks(
        Task(name="T1", period=20, deadline=7, execution_time=3),
        Task(name="T2", period=5, deadline=4, execution_time=2),
        Task(name="T3", period=10, deadline=8, execution_time=1),
        Task(name="T4", period=25, deadline=12, execution_time=3),
    )
    p4 = Processor("Least Laxity First", 4, LLF(), 100)
    p4.add_tasks(
        Task(name="T1", period=20, deadline=7, execution_time=3),
        Task(name="T2", period=5, deadline=4, execution_time=2),
        Task(name="T3", period=10, deadline=8, execution_time=1),
        Task(name="T4", period=25, deadline=12, execution_time=3),
    )
    p1.start()
    p2.start()
    p3.start()
    p4.start()


if __name__ == "__main__":
    main()

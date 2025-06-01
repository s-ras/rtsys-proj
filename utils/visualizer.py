# pyright: standard

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from colorhash import ColorHash as ch

if TYPE_CHECKING:
    from utils.core import Core
    from utils.record import Record


def visualize(
    name: str,
    cores: list[Core],
    xlim: int,
):
    fig, axes = plt.subplots(len(cores), 1, figsize=(15, 8), squeeze=False)
    fig.suptitle(name, fontsize=20, fontweight="bold", y=0.995)
    axes = axes.flatten()

    for core, ax in zip(cores, axes):
        if len(core.history) == 0:
            ax.set_title(f"Core #{core.id} (No jobs)")
            ax.axis("off")
            continue

        data: list[tuple[patches.Rectangle, Record]] = []

        for record in core.history:
            color = ch(record.job.task.name).hex
            name = f"{record.job.task.name} #{record.job.id}"

            duration = record.preemption_time - record.resumption_time
            rect = patches.Rectangle(
                (record.resumption_time, 0.25), duration, 0.5, color=color, alpha=0.8
            )
            ax.add_patch(rect)
            data.append((rect, record))
            ax.text(
                record.resumption_time + duration / 2,
                0.5,
                name,
                ha="center",
                va="center",
                color="black",
                fontsize=4,
                fontweight="bold",
            )

        ax.set_xlabel("Time")
        ax.set_title(f"Core #{core.id}")
        ax.set_xlim(0, xlim)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.grid(True, axis="x", linestyle="--", alpha=0.5)
        ax.set_xticks(range(0, xlim + 1))

        tooltip = ax.annotate(
            "",
            xy=(0, 0),
            xytext=(20, 20),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->"),
            ha="left",
            va="bottom",
            fontsize=9,
            visible=False,
        )

        def on_move(
            event,
            rectangles: list[tuple[patches.Rectangle, Record]] = data,
            tooltip=tooltip,
            ax=ax,
        ):
            visible = tooltip.get_visible()
            if event.inaxes == ax:
                for rect, record in rectangles:
                    contains, _ = rect.contains(event)
                    if contains:
                        tooltip.xy = (event.xdata, event.ydata)
                        tooltip.set_text(
                            f"name: {record.job.task.name}\n"
                            f"iteration: {record.job.id}\n"
                            f"start time: {record.job.start_time}\n"
                            f"finish time: {record.job.finish_time}\n"
                            f"release time: {record.job.release_time}\n"
                            f"remaining time: {record.job.remaining_time}\n"
                            f"laxity: {record.job.laxity}\n"
                            f"relative deadline: {record.job.relative_deadline}\n"
                            f"absolute deadline: {record.job.absolute_deadline}\n"
                            f"execution time: {record.job.task.execution_time}\n"
                            f"period: {record.job.task.period}\n"
                            f"priority: {record.record_priority}\n"
                            f"resumption time: {record.resumption_time}\n"
                            f"preemption time: {record.preemption_time}"
                        )
                        tooltip.set_visible(True)
                        fig.canvas.draw_idle()
                        return
            if visible:
                tooltip.set_visible(False)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", on_move)

    plt.tight_layout()
    plt.show()

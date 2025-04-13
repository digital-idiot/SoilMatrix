"""Module for tracking progress.

Helper classes for tracking progress.
"""
from typing import Any

from rich.console import RenderableType, StyleType, TextType
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    Task,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.text import Text

__all__ = ["DynamicSpinnerColumn", "TaskProgress"]

class DynamicSpinnerColumn(SpinnerColumn):
    """SpinnerColumn with optional stop state.

    This class is a modification of the original SpinnerColumn class to
     include an optional stop state.
    """
    def render(self, task: Task) -> RenderableType:
        """Render the spinner column.

        The  function to render the spinner column.

        If the task is finished, render the finished_text string. If the task
         has been stopped, render the stop_status field as a rich
         markup string. Otherwise, render the spinner itself.

        Args:
            task (Task): The task to render.

        Returns:
            RenderableType: The renderable object of the spinner column.
        """
        if task.finished:
            return self.finished_text
        elif (
            getattr(task, "stop_time", None) is not None
        ) and (
            task.fields.get("stop_status", None)
        ):
            return Text.from_markup(task.fields["stop_status"])
        else:
            return self.spinner.render(task.get_time())

class TaskProgress(Progress):
    """Customized Progress class.

    This class is a modification of the original Progress class to adopt a
     custom style and configuration.
    """
    def __init__(
        self,
        spinner_name: str = 'earth',
        spinner_finished_text: TextType = "✅",
        spinner_style: StyleType | None = 'progress.spinner',
        spinner_speed: float = 0.75,
        text_format: str = "{task.description}:",
        text_style: StyleType = "progress.description",
        bar_width: int | None =None,
        bar_style: StyleType = 'bar.back',
        complete_style: StyleType = 'bar.complete',
        finished_style: StyleType = 'bar.finished',
        pulse_style: StyleType = 'bar.pulse',
        progress_format: str = '[progress.percentage]{task.percentage:>3.0f}%',
        progress_format_no_percentage: str = '??:??',
        progress_style: StyleType = 'none',
        **kwargs: Any
    ) -> None:
        """Constructor for the TaskProgress class.

        Initialize the TaskProgress object.

        This is a customized version of the `rich.Progress` class.

        Args:
            spinner_name (str, optional): The name of the spinner. Defaults to
             'earth'.
            spinner_finished_text (TextType, optional): The text to render when
             the task is finished. Defaults to "✅".
            spinner_style (StyleType | None, optional): The style of the
             spinner. Defaults to 'progress.spinner'.
            spinner_speed (float, optional): The speed of the spinner.
             Defaults to 0.75.
            text_format (str, optional): The format of the text column.
             Defaults to "{task.description}:"
            text_style (StyleType, optional): The style of the text column.
             Defaults to "progress.description".
            bar_width (int | None, optional): The width of the bar column.
             Defaults to None.
            bar_style (StyleType, optional): The style of the bar column.
             Defaults to 'bar.back'.
            complete_style (StyleType, optional): The style of the bar column
             when the task is complete. Defaults to 'bar.complete'.
            finished_style (StyleType, optional): The style of the bar column
             when the task is finished. Defaults to 'bar.finished'.
            pulse_style (StyleType, optional): The style of the bar column when
             the task is pulsing. Defaults to 'bar.pulse'.
            progress_format (str, optional): The format of the progress column.
             Defaults to '[progress.percentage]{task.percentage:>3.0f}%'
            progress_format_no_percentage (str, optional): The format of the
             progress column when the task is not finished. Defaults to '??:??'
            progress_style (StyleType, optional): The style of the progress
             column. Defaults to 'none'.
            **kwargs: Any additional keyword arguments will be passed to the
             `rich.Progress` constructor.
        """
        super().__init__(
            DynamicSpinnerColumn(
                spinner_name=spinner_name,
                finished_text=spinner_finished_text,
                style=spinner_style,
                speed=spinner_speed
            ),
            TextColumn(
                text_format=text_format,
                style=text_style
            ),
            BarColumn(
                bar_width=bar_width,
                style=bar_style,
                complete_style=complete_style,
                finished_style=finished_style,
                pulse_style=pulse_style
            ),
            TaskProgressColumn(
                text_format=progress_format,
                text_format_no_percentage=progress_format_no_percentage,
                style=progress_style,
                show_speed=False
            ),
            TimeRemainingColumn(
                compact=False,
                elapsed_when_finished=True
            ),
            **kwargs
        )

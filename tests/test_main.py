import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from models import Task
from utils import format_task


def test_task_creation():
  task = Task("Test task")

  assert task.title == "Test task"
  assert task.completed is False


def test_task_completion():
  task = Task("Test task")

  task.complete()

  assert task.completed is True


def test_format_task():
  task = Task("Test task")

  assert "не выполнена" in format_task(task)
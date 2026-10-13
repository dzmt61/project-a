from dataclasses import dataclass


@dataclass
class Task:
  title: str
  description: str = ""
  completed: bool = False

  def complete(self):
    self.completed = True
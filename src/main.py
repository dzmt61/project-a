from models import Task
from utils import format_task


def main():
  task = Task(
    title="Подготовить лабораторную работу",
    description="Настроить взаимосвязанные Git-проекты"
  )

  print(format_task(task))

  task.complete()

  print(format_task(task))


if __name__ == "__main__":
  main()
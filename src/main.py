from models import Task
from utils import format_task

from date_utils import get_current_date, format_date
from string_utils import reverse_string, capitalize_words
from date_utils import bat_question

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
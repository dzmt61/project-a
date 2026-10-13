def format_task(task):
  status = "выполнена" if task.completed else "не выполнена"
  return f"{task.title}: {status}"
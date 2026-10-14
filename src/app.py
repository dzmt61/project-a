import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from date_utils import get_current_date, format_date
from string_utils import reverse_string, capitalize_words
from file_utils import write_text_file, read_text_file, get_file_info
from logger_utils import get_logger


app = Flask(__name__, template_folder="../templates")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_FILE = BASE_DIR / "logs" / "app.log"
TEXT_FILE = DATA_DIR / "user_text.txt"
DATABASE_FILE = DATA_DIR / "tasks.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logger = get_logger(
    name="project_a",
    log_file=str(LOG_FILE),
)


def get_db_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                due_date TEXT NOT NULL DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def get_tasks(status="all"):
    query = "SELECT * FROM tasks"
    parameters = ()

    if status == "active":
        query += " WHERE completed = 0"
    elif status == "completed":
        query += " WHERE completed = 1"

    query += """
        ORDER BY
            completed ASC,
            CASE WHEN due_date = '' THEN 1 ELSE 0 END,
            due_date ASC,
            id DESC
    """

    with get_db_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()

    return [dict(row) for row in rows]


def get_task_counts():
    with get_db_connection() as connection:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN completed = 0 THEN 1 ELSE 0 END) AS active,
                SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) AS completed
            FROM tasks
            """
        ).fetchone()

    return {
        "total": row["total"] or 0,
        "active": row["active"] or 0,
        "completed": row["completed"] or 0,
    }


def render_home(result=None, error=None, status="all"):
    return render_template(
        "index.html",
        result=result,
        error=error,
        tasks=get_tasks(status),
        counts=get_task_counts(),
        current_status=status,
    )


init_database()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    status = request.args.get("status", "all")

    if status not in {"all", "active", "completed"}:
        status = "all"

    if request.method == "POST":
        operation = request.form.get("operation", "")
        value = request.form.get("value", "")

        try:
            # Управление задачами
            if operation == "create_task":
                title = request.form.get("title", "").strip()
                description = request.form.get("description", "").strip()
                due_date = request.form.get("due_date", "").strip()

                if not title:
                    raise ValueError("Введите название задачи.")

                with get_db_connection() as connection:
                    connection.execute(
                        """
                        INSERT INTO tasks (title, description, due_date)
                        VALUES (?, ?, ?)
                        """,
                        (title, description, due_date),
                    )

                result = "Задача добавлена."
                logger.info("Создана задача: %s", title)

            elif operation == "update_task":
                task_id = request.form.get("task_id", type=int)
                title = request.form.get("title", "").strip()
                description = request.form.get("description", "").strip()
                due_date = request.form.get("due_date", "").strip()

                if not task_id:
                    raise ValueError("Не указан идентификатор задачи.")
                if not title:
                    raise ValueError("Название задачи не может быть пустым.")

                with get_db_connection() as connection:
                    cursor = connection.execute(
                        """
                        UPDATE tasks
                        SET title = ?, description = ?, due_date = ?
                        WHERE id = ?
                        """,
                        (title, description, due_date, task_id),
                    )

                if cursor.rowcount == 0:
                    raise ValueError("Задача не найдена.")

                result = "Изменения задачи сохранены."
                logger.info("Обновлена задача с ID %s", task_id)

            elif operation == "toggle_task":
                task_id = request.form.get("task_id", type=int)

                if not task_id:
                    raise ValueError("Не указан идентификатор задачи.")

                with get_db_connection() as connection:
                    cursor = connection.execute(
                        """
                        UPDATE tasks
                        SET completed = CASE completed
                            WHEN 0 THEN 1 ELSE 0
                        END
                        WHERE id = ?
                        """,
                        (task_id,),
                    )

                if cursor.rowcount == 0:
                    raise ValueError("Задача не найдена.")

                result = "Статус задачи изменён."
                logger.info("Изменён статус задачи с ID %s", task_id)

            elif operation == "delete_task":
                task_id = request.form.get("task_id", type=int)

                if not task_id:
                    raise ValueError("Не указан идентификатор задачи.")

                with get_db_connection() as connection:
                    cursor = connection.execute(
                        "DELETE FROM tasks WHERE id = ?",
                        (task_id,),
                    )

                if cursor.rowcount == 0:
                    raise ValueError("Задача не найдена.")

                result = "Задача удалена."
                logger.info("Удалена задача с ID %s", task_id)

            # Существующие операции Project B — оставлены без изменения
            elif operation == "current_date":
                result = get_current_date()

            elif operation == "format_date":
                result = format_date(value)

            elif operation == "reverse":
                result = reverse_string(value)

            elif operation == "capitalize":
                result = capitalize_words(value)

            elif operation == "save_file":
                write_text_file(str(TEXT_FILE), value)
                result = f"Текст сохранён в файл: {TEXT_FILE.name}"

            elif operation == "read_file":
                result = read_text_file(str(TEXT_FILE))

            elif operation == "file_info":
                info = get_file_info(str(TEXT_FILE))
                result = (
                    f"Имя: {info['name']}; "
                    f"Размер: {info['size']} байт; "
                    f"Расширение: {info['extension']}"
                )

            else:
                raise ValueError("Неизвестная операция.")

            logger.info("Выполнена операция: %s", operation)

        except (ValueError, FileNotFoundError) as exc:
            error = str(exc)
            logger.warning("Ошибка операции %s: %s", operation, exc)

        except Exception:
            logger.exception("Непредвиденная ошибка операции %s", operation)
            error = "Внутренняя ошибка приложения."

    return render_home(result=result, error=error, status=status)


@app.route("/api/date")
def api_date():
    logger.info("Вызван API текущей даты")
    return jsonify({"date": get_current_date()})


@app.route("/api/format-date")
def api_format_date():
    value = request.args.get("date", "")

    try:
        formatted = format_date(value)
        logger.info("Вызван API форматирования даты")
        return jsonify({"formatted_date": formatted})
    except ValueError:
        return jsonify({
            "error": "Укажите дату в формате YYYY-MM-DD"
        }), 400


@app.route("/api/reverse")
def api_reverse():
    value = request.args.get("text", "")
    logger.info("Вызван API обработки строки")
    return jsonify({"result": reverse_string(value)})


@app.route("/api/tasks")
def api_tasks():
    """Возвращает список задач в формате JSON."""
    status = request.args.get("status", "all")

    if status not in {"all", "active", "completed"}:
        return jsonify({"error": "Недопустимый фильтр задач."}), 400

    return jsonify({"tasks": get_tasks(status), "counts": get_task_counts()})


if __name__ == "__main__":
    app.run(debug=True)


from pathlib import Path

from flask import Flask, jsonify, render_template, request

from date_utils import get_current_date, format_date
from string_utils import reverse_string, capitalize_words
from file_utils import write_text_file, read_text_file, get_file_info
from logger_utils import get_logger


app = Flask(
    __name__,
    template_folder="../templates",
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_FILE = BASE_DIR / "logs" / "app.log"
TEXT_FILE = DATA_DIR / "user_text.txt"

logger = get_logger(
    name="project_a",
    log_file=str(LOG_FILE),
)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        operation = request.form.get("operation", "")
        value = request.form.get("value", "")

        try:
            if operation == "current_date":
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
                result = get_file_info(str(TEXT_FILE))
                result = (
                    f"Имя: {result['name']}; "
                    f"Размер: {result['size']} байт; "
                    f"Расширение: {result['extension']}"
                )

            else:
                raise ValueError("Неизвестная операция")

            logger.info("Выполнена операция: %s", operation)

        except (ValueError, FileNotFoundError) as exc:
            error = str(exc)
            logger.warning(
                "Ошибка операции %s: %s",
                operation,
                exc,
            )

        except Exception:
            logger.exception(
                "Непредвиденная ошибка операции %s",
                operation,
            )
            error = "Внутренняя ошибка приложения"

    return render_template(
        "index.html",
        result=result,
        error=error,
    )


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


if __name__ == "__main__":
    app.run(debug=True)

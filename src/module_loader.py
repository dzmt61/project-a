import sys
from pathlib import Path


PROJECT_B_SRC = (
    Path(__file__).resolve().parents[1]
    / "libs"
    / "project-b"
    / "src"
)

sys.path.insert(0, str(PROJECT_B_SRC))

from date_utils import get_current_date
from string_utils import (
    reverse_string,
    capitalize_words,
)


def main():
    print(f"Текущая дата: {get_current_date()}")
    print(f"Обратный текст: {reverse_string('Hello World')}")
    print(
        f"С заглавной: "
        f"{capitalize_words('hello world from project a')}"
    )


if __name__ == "__main__":
    main()
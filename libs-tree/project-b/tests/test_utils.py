from datetime import date

from project_b_utils import (
  get_current_date,
  format_date,
  reverse_string,
  capitalize_words,
)


def test_get_current_date():
  result = get_current_date()

  assert isinstance(result, str)
  assert len(result) == 10


def test_format_date():
  result = format_date(date(2026, 10, 6))

  assert result == "06.10.2026"


def test_reverse_string():
  assert reverse_string("Hello") == "olleH"


def test_capitalize_words():
  assert capitalize_words("hello world") == "Hello World"
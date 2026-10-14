def reverse_string(value):
  return value[::-1]


def capitalize_words(value):
  return " ".join(word.capitalize() for word in value.split())
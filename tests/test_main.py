
from src.app import app


def setup_module():
    app.config["TESTING"] = True


def test_home_page():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert "Project A".encode() in response.data


def test_current_date_api():
    client = app.test_client()
    response = client.get("/api/date")

    assert response.status_code == 200
    assert "date" in response.get_json()


def test_format_date_api():
    client = app.test_client()
    response = client.get("/api/format-date?date=2026-10-14")

    assert response.status_code == 200
    assert response.get_json()["formatted_date"] == "14.10.2026"


def test_invalid_date_api():
    client = app.test_client()
    response = client.get("/api/format-date?date=invalid")

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_reverse_string_api():
    client = app.test_client()
    response = client.get("/api/reverse?text=hello")

    assert response.status_code == 200
    assert response.get_json()["result"] == "olleh"


def test_string_operation_in_web_interface():
    client = app.test_client()

    response = client.post(
        "/",
        data={
            "operation": "capitalize",
            "value": "hello world",
        },
    )

    assert response.status_code == 200
    assert b"Hello World" in response.data


def test_file_operations_in_web_interface():
    client = app.test_client()

    # Сначала сохраняем текст.
    response = client.post(
        "/",
        data={
            "operation": "save_file",
            "value": "Integration test text",
        },
    )
    assert response.status_code == 200
    assert "Текст сохранён".encode() in response.data

    # Затем читаем сохранённый текст.
    response = client.post(
        "/",
        data={"operation": "read_file"},
    )
    assert response.status_code == 200
    assert b"Integration test text" in response.data

    # Проверяем получение информации о файле.
    response = client.post(
        "/",
        data={"operation": "file_info"},
    )
    assert response.status_code == 200
    assert b"user_text.txt" in response.data


def test_logging_integration():
    client = app.test_client()
    response = client.get("/api/date")

    assert response.status_code == 200

    from src.app import LOG_FILE

    assert LOG_FILE.exists()
    assert "API текущей даты" in LOG_FILE.read_text(
        encoding="utf-8"
    )

# Project A — Приложение для работы с утилитами

# 1. Описание проекта

Project A веб-приложение на Flask, предоставляющее пользовательский интерфейс для работы с утилитами Python.

Приложение демонстрирует интеграцию двух независимо организованных проектов: веб-приложения Project A и библиотеки Project B. Пользователь может выполнять операции с датами и строками, работать с текстовыми файлами и обращаться к функциям через HTTP API.

Пользовательский интерфейс реализован с использованием HTML и Tailwind CSS.

# 2. Структура проекта

```bash
project-a/
├── src/
│   └── app.py
├── templates/
│   └── index.html
├── uploads/
│   └── ...
├── libs/
│   └── project-b/
│       ├── src/
│       │   ├── date_utils.py
│       │   ├── string_utils.py
│       │   ├── file_utils.py
│       │   └── logger_utils.py
│       └── setup.py
├── tests/
│   └── test_main.py
├── .gitmodules
├── requirements.txt
├── pytest.ini
└── README.md
```

# 3. Получение исходного кода

Если Project A уже клонирован, перейдите в его корневой каталог.

При первоначальном клонировании репозитория с подключённым Git-субмодулем используйте:

```bash
git clone --recurse-submodules <URL-репозитория-Project-A>
cd project-a
```

Если репозиторий уже клонирован без субмодулей:

```bash
git submodule update --init --recursive
```

Проверить состояние субмодуля можно командой:

```bash
git submodule status
```

Project B подключён как отдельный Git-репозиторий. Его изменения фиксируются в собственном репозитории, а Project A хранит ссылку на конкретную версию субмодуля.

4. Установка и настройка

Создайте виртуальное окружение из корня Project A:

```bash
python -m venv .venv
```

Активируйте его в Windows CMD:

```bash
.venv\Scripts\activate.bat
```

В PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

В Git Bash:

```bash
source .venv/Scripts/activate
```

Обновите установщик пакетов:

```bash
python -m pip install --upgrade pip
```

Установите зависимости:

```bash
python -m pip install -r requirements.txt
```

Если Project B ещё не установлен в активном виртуальном окружении, его можно подключить в режиме разработки:

```bash
python -m pip install -e libs/project-b
```

Этот способ предполагает, что в каталоге libs/project-b находится корректный setup.py.

5. Запуск приложения

Из корня Project A выполните:

```bash
python src/app.py
```

Откройте адрес, указанный Flask в терминале. По умолчанию это обычно:

```
http://127.0.0.1:5000/
```

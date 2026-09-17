# krivoruchko-dev.ru

Стартовая страница (dashboard) для self-hosted сервисов домашнего сервера. Одна главная страница со ссылками на Jellyfin, Vaultwarden, Nextcloud и другие сервисы — удобная «домашняя» точка входа вместо закладок.

Сайт: [krivoruchko-dev.ru](https://krivoruchko-dev.ru/)

## Возможности

- Карточки сервисов с названием, описанием, цветом акцента и иконкой
- Список сервисов задаётся в JSON без правок Python-кода
- Проверка доступности URL (HEAD/GET) с кэшем и обновлением по кнопке
- Счётчик посещений главной страницы (SQLite в пользовательской директории ОС)
- Эндпоинт `/health` для мониторинга без учёта визитов
- Адаптивная вёрстка, тёмная тема

## Стек

- [Flask](https://flask.palletsprojects.com/) 3.x
- [platformdirs](https://github.com/platformdirs/platformdirs) — каталог данных приложения
- Jinja2 + CSS в `static/css/dashboard.css`

## Структура проекта

```
krivoruchko-dev.ru/
├── app/
│   ├── __init__.py      # create_app()
│   ├── routes.py        # маршруты /, /health, /api/health
│   ├── services.py      # загрузка и валидация services.json
│   ├── visits.py        # счётчик в SQLite
│   └── health.py        # проверка доступности сервисов
├── config.py            # настройки и переменные окружения
├── main.py              # точка входа, объект app для WSGI
├── services.json
├── templates/
│   └── index.html
├── static/
│   ├── css/dashboard.css
│   └── icons/
├── tests/
└── requirements.txt
```

## Требования

- Python 3.10+
- Зависимости из `requirements.txt`

## Установка и запуск

```bash
cd krivoruchko-dev.ru
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python main.py
```

По умолчанию: `http://127.0.0.1:5000/`.

Продакшен (waitress на Windows):

```bash
pip install waitress
waitress-serve --listen=127.0.0.1:8080 main:app
```

## Переменные окружения

| Переменная             | По умолчанию              | Описание                                                          |
| ---------------------- | ------------------------- | ----------------------------------------------------------------- |
| `SITE_NAME`            | `home · server`           | Заголовок на странице                                             |
| `PAGE_TITLE`           | `Home Server · Dashboard` | `<title>`                                                         |
| `SERVICES_FILE`        | `./services.json`         | Путь к конфигу сервисов                                           |
| `FLASK_HOST`           | `127.0.0.1`               | Хост dev-сервера                                                  |
| `FLASK_PORT`           | `5000`                    | Порт dev-сервера                                                  |
| `FLASK_DEBUG`          | выкл.                     | `1` / `true` для debug                                            |
| `HEALTH_CHECK_TIMEOUT` | `3`                       | Таймаут проверки URL (сек)                                        |
| `HEALTH_CHECK_TTL`     | `60`                      | Кэш результатов health-check (сек)                                |
| `HEALTH_STRICT`        | выкл.                     | Только 2xx/3xx; иначе 401/403 тоже «доступен» (Basic Auth и т.п.) |

## Настройка сервисов

Файл `services.json` — объект, ключи произвольные (идентификаторы). Для каждого сервиса:

| Поле            | Обязательное | Описание                                                          |
| --------------- | ------------ | ----------------------------------------------------------------- |
| `name`          | да           | Имя на карточке                                                   |
| `url`           | да           | Ссылка (новая вкладка)                                            |
| `description`   | нет          | Подпись                                                           |
| `color`         | нет          | CSS-цвет акцента (`#6c8cff` по умолчанию)                         |
| `icon`          | нет          | Файл в `static/icons/`                                            |
| `health_url`    | нет          | Отдельный URL для проверки (по умолчанию — `url`)                 |
| `health_strict` | нет          | `true` — для сервиса только 2xx/3xx (перекрывает `HEALTH_STRICT`) |

Пустой `color` автоматически заменяется на цвет по умолчанию.

Сервисы с паролем (Transmission за reverse proxy и т.д.) обычно отвечают **401** без cookies — в режиме по умолчанию это считается «доступен».

## API

- `GET /` — dashboard (увеличивает счётчик визитов)
- `GET /health` — `{"status":"ok"}` для балансировщика/мониторинга
- `GET /api/health` — `{"all_up": bool, "services": {"id": bool, ...}}` (принудительная проверка)

## Счётчик посещений

Хранится в SQLite (`visits.db`) в каталоге данных приложения (`platformdirs`), например:

- **Windows:** `%LOCALAPPDATA%\krivoruchko-dev\krivoruchko-dev\visits.db`
- **Linux:** `~/.local/share/krivoruchko-dev/visits.db` (зависит от XDG)

## Тесты

```bash
python -m unittest discover -s tests -v
```

## Развёртывание

1. `pip install -r requirements.txt`
2. Иконки в `static/icons/`
3. Проверьте URL в `services.json`
4. Запуск `main:app` за reverse proxy с HTTPS

Путь к `services.json` задаётся относительно `config.BASE_DIR`, а не текущей рабочей директории процесса (если не переопределён `SERVICES_FILE`).

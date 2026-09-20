# krivoruchko-dev.ru

A simple Flask dashboard for my home server. Shows self-hosted services with health status, server uptime, and a visit counter.

## Services

Configured via `services.json`:

## Run

```bash
pip install -r requirements.txt
python main.py
```

Dashboard will be available at `http://127.0.0.1:5000`.

## Configuration

Environment variables (optional):

| Variable               | Default                                                   | Description                      |
| ---------------------- | --------------------------------------------------------- | -------------------------------- |
| `FLASK_HOST`           | `127.0.0.1`                                               | Listen address                   |
| `FLASK_PORT`           | `5000`                                                    | Listen port                      |
| `FLASK_DEBUG`          | `false`                                                   | Debug mode                       |
| `SERVICES_FILE`        | `./services.json`                                         | Path to services config          |
| `HEALTH_CHECK_TIMEOUT` | `3`                                                       | Health check timeout (seconds)   |
| `HEALTH_CHECK_TTL`     | `60`                                                      | Health check cache TTL (seconds) |
| `HEALTH_STRICT`        | `false`                                                   | Treat 401/403 as down            |
| `GITHUB_URL`           | `https://github.com/olegkrivoruchko93/krivoruchko-dev.ru` | Repository for this page         |

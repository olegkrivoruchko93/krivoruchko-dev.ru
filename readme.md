# krivoruchko-dev.ru

A simple Flask dashboard for my home server. Shows self-hosted services with health status, server uptime, and a visit counter.

## Services

Configured via `services.json`:

| Service      | Description    |
| ------------ | -------------- |
| Jellyfin     | Media server   |
| VaultWarden  | Password manager |
| Transmission | Torrent client |
| NextCloud    | Cloud storage  |

## Installation

```bash
git clone https://github.com/olegkrivoruchko93/krivoruchko-dev.ru.git
cd krivoruchko-dev.ru
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run (manual)

```bash
source venv/bin/activate
python main.py
```

Dashboard will be available at `http://127.0.0.1:5000`.

## Run (systemd service)

Create `/etc/systemd/system/krivoruchko-dev.service`:

```ini
[Unit]
Description=krivoruchko-dev.ru dashboard
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/krivoruchko-dev.ru
ExecStart=/opt/krivoruchko-dev.ru/venv/bin/python main.py
Restart=on-failure
RestartSec=5
Environment=FLASK_HOST=0.0.0.0
Environment=FLASK_PORT=5000

[Install]
WantedBy=multi-user.target
```

Then enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable krivoruchko-dev
sudo systemctl start krivoruchko-dev
```

## Configuration

Environment variables (optional):

| Variable               | Default | Description                      |
| ---------------------- | ------- | -------------------------------- |
| `FLASK_HOST`           | `127.0.0.1` | Listen address               |
| `FLASK_PORT`           | `5000`  | Listen port                      |
| `FLASK_DEBUG`          | `false` | Debug mode                       |
| `SERVICES_FILE`        | `./services.json` | Path to services config  |
| `HEALTH_CHECK_TIMEOUT` | `3`     | Health check timeout (seconds)   |
| `HEALTH_CHECK_TTL`     | `60`    | Health check cache TTL (seconds) |
| `HEALTH_STRICT`        | `false` | Treat 401/403 as down            |

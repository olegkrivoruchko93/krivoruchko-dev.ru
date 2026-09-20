import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DEFAULT_ACCENT = "#6c8cff"

SERVICES_FILE = Path(
    os.environ.get("SERVICES_FILE", str(BASE_DIR / "services.json"))
)

FLASK_HOST = os.environ.get("FLASK_HOST", "127.0.0.1")
FLASK_PORT = int(os.environ.get("FLASK_PORT", "5000"))
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")

HEALTH_CHECK_TIMEOUT = float(os.environ.get("HEALTH_CHECK_TIMEOUT", "3"))
HEALTH_CHECK_TTL = float(os.environ.get("HEALTH_CHECK_TTL", "60"))
# If false, HTTP 401/403 count as reachable (auth-protected apps like Transmission).
HEALTH_STRICT = os.environ.get("HEALTH_STRICT", "").lower() in ("1", "true", "yes")

DATA_APP_NAME = "krivoruchko-dev"
DATA_APP_AUTHOR = "krivoruchko-dev"
GITHUB_URL = os.environ.get("GITHUB_URL", "https://github.com/olegkrivoruchko93/krivoruchko-dev.ru")
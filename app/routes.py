from flask import render_template, request

from app.health import check_services
from app.services import load_services
from app.visits import record_visit
from datetime import datetime, timezone
import time
from config import GITHUB_URL
import psutil


def register_routes(app):
    @app.get("/")
    def index():
        visit_count = record_visit(
            request.remote_addr, datetime.now(timezone.utc).isoformat())
        services = load_services()
        uptimeSeconds = time.time() - psutil.boot_time()
        uptime = time.strftime('%dd %Hh %Mm', time.gmtime(uptimeSeconds))

        return render_template(
            "index.html",
            services=services,
            visit_count=visit_count,
            service_statuses=check_services(services),
            uptime=uptime,
            github_url=GITHUB_URL
        )

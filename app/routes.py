from flask import Blueprint, jsonify, render_template

from app.health import check_services
from app.services import load_services
from app.visits import increment_visit_count
from config import PAGE_TITLE, SITE_NAME

bp = Blueprint("dashboard", __name__)


@bp.get("/")
def index():
    services = load_services()
    visit_count = increment_visit_count()
    all_up, service_statuses = check_services(services)

    return render_template(
        "index.html",
        services=services,
        visit_count=visit_count,
        all_up=all_up,
        service_statuses=service_statuses,
        site_name=SITE_NAME,
        title=PAGE_TITLE,
    )


@bp.get("/health")
def health():
    return jsonify(status="ok")


@bp.get("/api/health")
def api_health():
    services = load_services()
    all_up, statuses = check_services(services, force=True)
    return jsonify(all_up=all_up, services=statuses)

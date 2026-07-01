from django.db import connection
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health_check(request):
    """
    GET /api/v1/health

    Deliberately NOT behind JWT auth and NOT wrapped in the standard
    {success, data} envelope -- infra tools (load balancers, uptime
    monitors, k8s probes) expect a plain, unauthenticated, fixed-shape
    response at this exact path, per the Module 1 spec.

    Actually exercises the DB connection (SELECT 1) rather than assuming
    it's up, so `db` reflects reality.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
        db_connected = True
    except OperationalError:
        db_connected = False

    body = {
        "status": "ok" if db_connected else "error",
        "db": "connected" if db_connected else "disconnected",
    }
    return JsonResponse(body, status=200 if db_connected else 503)

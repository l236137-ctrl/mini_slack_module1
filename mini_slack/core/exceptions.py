from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler as drf_exception_handler

ERROR_CODES = {
    400: "VALIDATION_ERROR",
    401: "NOT_AUTHENTICATED",
    403: "PERMISSION_DENIED",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
    429: "RATE_LIMITED",
    500: "SERVER_ERROR",
}


def envelope_exception_handler(exc, context):
    """
    Project-wide DRF exception handler. Converts whatever DRF's default
    handler produces into the standard error envelope:

      {"success": false, "error": {"code": "...", "message": "...", "fields": {...}}}

    `fields` is only populated for validation errors (400s tied to specific
    request fields); every other error type gets an empty fields dict.
    """
    response = drf_exception_handler(exc, context)

    if response is None:
        # Not a DRF/Django exception DRF knows how to handle (i.e. a genuine
        # unhandled bug) -- let it propagate so Django's normal 500 handling
        # (and DEBUG tracebacks locally) still applies.
        return None

    code = ERROR_CODES.get(response.status_code, "ERROR")
    fields = {}
    detail = response.data

    if isinstance(exc, ValidationError) and isinstance(detail, dict):
        for field, errors in detail.items():
            if isinstance(errors, (list, tuple)):
                fields[field] = " ".join(str(e) for e in errors)
            else:
                fields[field] = str(errors)
        message = "One or more fields failed validation."
    elif isinstance(detail, dict) and "detail" in detail:
        message = str(detail["detail"])
    elif isinstance(detail, list):
        message = " ".join(str(e) for e in detail)
    else:
        message = str(detail)

    response.data = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "fields": fields,
        },
    }
    return response

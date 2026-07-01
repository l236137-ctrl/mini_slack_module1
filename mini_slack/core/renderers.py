from rest_framework.renderers import JSONRenderer


class EnvelopeJSONRenderer(JSONRenderer):
    """
    Wraps every DRF response in the project-wide standard envelope so
    individual views never have to remember to build it themselves:

      success: {"success": true,  "data": {...}}
      error:   {"success": false, "error": {"code": ..., "message": ..., "fields": {...}}}

    Error shaping happens in core.exceptions.envelope_exception_handler;
    this renderer just passes those through untouched and wraps everything
    else as a success payload.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        renderer_context = renderer_context or {}
        response = renderer_context.get("response")

        if isinstance(data, dict) and "success" in data:
            # Already shaped by the exception handler (or a view that
            # deliberately returns a pre-built envelope).
            payload = data
        elif response is not None and getattr(response, "exception", False):
            # Defensive fallback in case an exception ever reaches the
            # renderer without going through envelope_exception_handler.
            payload = {
                "success": False,
                "error": {
                    "code": "ERROR",
                    "message": data if isinstance(data, str) else "An error occurred.",
                    "fields": data if isinstance(data, dict) else {},
                },
            }
        else:
            payload = {"success": True, "data": data}

        return super().render(payload, accepted_media_type, renderer_context)

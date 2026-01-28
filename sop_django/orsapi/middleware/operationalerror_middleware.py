from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse


class DatabaseDownMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # ✅ Allow CORS preflight requests
        if request.method == "OPTIONS":
            return self.get_response(request)

        # ✅ Only check DB for API URLs (optional but recommended)
        if request.path.startswith("/orsapi/"):
            try:
                connections['default'].cursor()
            except OperationalError:
                return JsonResponse(
                    {
                        "success": False,
                        "result": {
                            "message": "Database service is currently unavailable. Please try again later."
                        }
                    },
                    status=200
                )

        return self.get_response(request)

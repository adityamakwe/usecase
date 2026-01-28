from django.conf import settings
from django.http import JsonResponse
from ..utility import JwtUtility


class JWTMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip token validation for certain URLs if needed
        # if request.path_info in ['/orsapi/Login/', '/orsapi/token/', '/orsapi/validate/','/orsapi/signup/']:
        #     return self.get_response(request)
        if request.path_info.startswith("/orsapi/Login") \
                or request.path_info.startswith("/orsapi/token") \
                or request.path_info.startswith("/orsapi/validate") \
                or request.path_info.startswith("/orsapi/ForgetPassword") \
                or request.path_info.startswith("/orsapi/signup"):
            return self.get_response(request)

        auth_header = request.headers.get('Authorization', '').split()

        if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
            return JsonResponse({'error': 'Invalid Authorization... plz login again..!!'}, status=401)

        token = auth_header[1]

        token_payload = JwtUtility.validate_jwt_token(token)

        if 'error' in token_payload:
            return JsonResponse(token_payload, status=401)

        request.user = token_payload

        return self.get_response(request)
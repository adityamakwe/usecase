from datetime import datetime, timedelta
import jwt
from django.conf import settings


def generate_jwt_token(loginId):
    # Define the payload (content of the token)
    payload = {
        'user_id': loginId,
        'exp': datetime.utcnow() + timedelta(days=1),  # Expiry datetime
        'iat': datetime.utcnow()  # Issued datetime
    }

    # Create the JWT token with the payload and the secret key
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def validate_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Handle case where JWT has expired
        return {'error': 'Token is expired... plz login again..!!'}
    except jwt.DecodeError:
        # Handle case where JWT is invalid (e.g., tampered with)
        return {'error': 'Token is Invalid... plz login again..!!'}
    except Exception as e:
        # Log the actual exception for debugging purposes
        return {'error': 'Failed to decode token'}
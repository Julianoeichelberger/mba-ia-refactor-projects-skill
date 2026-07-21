from functools import wraps

import jwt
from flask import request, g

from middlewares.error_handler import AppError
from utils.jwt_service import decode_token


def auth_required(roles=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            header = request.headers.get('Authorization', '')
            if not header.startswith('Bearer '):
                raise AppError('Authorization token required', 401)

            token = header.split(' ', 1)[1].strip()
            try:
                payload = decode_token(token)
            except jwt.ExpiredSignatureError:
                raise AppError('Token expired', 401)
            except jwt.InvalidTokenError:
                raise AppError('Invalid token', 401)

            g.user_id = int(payload['sub'])
            g.user_role = payload.get('role')

            if roles and g.user_role not in roles:
                raise AppError('Insufficient permissions', 403)

            return fn(*args, **kwargs)
        return wrapper
    return decorator

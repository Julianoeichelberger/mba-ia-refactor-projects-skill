from datetime import datetime, timedelta, timezone

import jwt

from config.settings import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_MINUTES


def generate_token(user):
    now = datetime.now(timezone.utc)
    payload = {
        'sub': str(user.id),
        'role': user.role,
        'iat': now,
        'exp': now + timedelta(minutes=JWT_EXP_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token):
    # Raises jwt.ExpiredSignatureError / jwt.InvalidTokenError on bad tokens.
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

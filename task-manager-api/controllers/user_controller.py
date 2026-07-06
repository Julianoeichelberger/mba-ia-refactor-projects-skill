import logging
import re

from models.database import db
from models.user import User
from models.task import Task
from middlewares.error_handler import AppError
from config.settings import VALID_ROLES, MIN_PASSWORD_LENGTH

logger = logging.getLogger(__name__)

EMAIL_REGEX = r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$'


class UserController:

    def get_all(self):
        users = User.query.all()
        result = []
        for u in users:
            data = u.to_dict()
            data['task_count'] = len(u.tasks)
            result.append(data)
        return result

    def get_by_id(self, user_id):
        user = User.query.get(user_id)
        if not user:
            raise AppError('User not found', 404)

        data = user.to_dict()
        data['tasks'] = [t.to_dict() for t in user.tasks]
        return data

    def create(self, data):
        if not data:
            raise AppError('Invalid data')

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')

        if not name:
            raise AppError('Name is required')
        if not email:
            raise AppError('Email is required')
        if not password:
            raise AppError('Password is required')

        if not re.match(EMAIL_REGEX, email):
            raise AppError('Invalid email')

        if len(password) < MIN_PASSWORD_LENGTH:
            raise AppError(f'Password must be at least {MIN_PASSWORD_LENGTH} characters')

        if User.query.filter_by(email=email).first():
            raise AppError('Email already registered', 409)

        if role not in VALID_ROLES:
            raise AppError('Invalid role')

        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        user.role = role

        db.session.add(user)
        db.session.commit()
        logger.info("User created: %d - %s", user.id, user.name)
        return user.to_dict()

    def update(self, user_id, data):
        user = User.query.get(user_id)
        if not user:
            raise AppError('User not found', 404)

        if not data:
            raise AppError('Invalid data')

        if 'name' in data:
            user.name = data['name']

        if 'email' in data:
            if not re.match(EMAIL_REGEX, data['email']):
                raise AppError('Invalid email')
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                raise AppError('Email already registered', 409)
            user.email = data['email']

        if 'password' in data:
            if len(data['password']) < MIN_PASSWORD_LENGTH:
                raise AppError('Password too short')
            user.set_password(data['password'])

        if 'role' in data:
            if data['role'] not in VALID_ROLES:
                raise AppError('Invalid role')
            user.role = data['role']

        if 'active' in data:
            user.active = data['active']

        db.session.commit()
        return user.to_dict()

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            raise AppError('User not found', 404)

        Task.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        logger.info("User deleted: %d", user_id)
        return {'message': 'User deleted successfully'}

    def get_user_tasks(self, user_id):
        user = User.query.get(user_id)
        if not user:
            raise AppError('User not found', 404)

        tasks = Task.query.filter_by(user_id=user_id).all()
        return [t.to_dict() for t in tasks]

    def login(self, data):
        if not data:
            raise AppError('Invalid data')

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise AppError('Email and password are required')

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            raise AppError('Invalid credentials', 401)

        if not user.active:
            raise AppError('User is inactive', 403)

        return {
            'message': 'Login successful',
            'user': user.to_dict(),
            'token': 'fake-jwt-token-' + str(user.id),
        }

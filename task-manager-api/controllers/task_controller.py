import logging
from datetime import datetime, timezone

from models.database import db
from models.task import Task
from models.user import User
from models.category import Category
from middlewares.error_handler import AppError
from config.settings import VALID_STATUSES, MIN_TITLE_LENGTH, MAX_TITLE_LENGTH

logger = logging.getLogger(__name__)


class TaskController:

    def get_all(self):
        tasks = Task.query.all()
        return [t.to_dict() for t in tasks]

    def get_by_id(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            raise AppError('Task not found', 404)
        return task.to_dict()

    def create(self, data):
        if not data:
            raise AppError('Invalid data')

        title = data.get('title')
        if not title:
            raise AppError('Title is required')
        if len(title) < MIN_TITLE_LENGTH:
            raise AppError('Title too short')
        if len(title) > MAX_TITLE_LENGTH:
            raise AppError('Title too long')

        status = data.get('status', 'pending')
        if status not in VALID_STATUSES:
            raise AppError('Invalid status')

        priority = data.get('priority', 3)
        if priority < 1 or priority > 5:
            raise AppError('Priority must be between 1 and 5')

        user_id = data.get('user_id')
        if user_id and not User.query.get(user_id):
            raise AppError('User not found', 404)

        category_id = data.get('category_id')
        if category_id and not Category.query.get(category_id):
            raise AppError('Category not found', 404)

        task = Task()
        task.title = title
        task.description = data.get('description', '')
        task.status = status
        task.priority = priority
        task.user_id = user_id
        task.category_id = category_id

        due_date = data.get('due_date')
        if due_date:
            try:
                task.due_date = datetime.strptime(due_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            except ValueError:
                raise AppError('Invalid date format. Use YYYY-MM-DD')

        tags = data.get('tags')
        if tags:
            task.tags = ','.join(tags) if isinstance(tags, list) else tags

        db.session.add(task)
        db.session.commit()
        logger.info("Task created: %d - %s", task.id, task.title)
        return task.to_dict()

    def update(self, task_id, data):
        task = Task.query.get(task_id)
        if not task:
            raise AppError('Task not found', 404)

        if not data:
            raise AppError('Invalid data')

        if 'title' in data:
            if len(data['title']) < MIN_TITLE_LENGTH:
                raise AppError('Title too short')
            if len(data['title']) > MAX_TITLE_LENGTH:
                raise AppError('Title too long')
            task.title = data['title']

        if 'description' in data:
            task.description = data['description']

        if 'status' in data:
            if data['status'] not in VALID_STATUSES:
                raise AppError('Invalid status')
            task.status = data['status']

        if 'priority' in data:
            if data['priority'] < 1 or data['priority'] > 5:
                raise AppError('Priority must be between 1 and 5')
            task.priority = data['priority']

        if 'user_id' in data:
            if data['user_id'] and not User.query.get(data['user_id']):
                raise AppError('User not found', 404)
            task.user_id = data['user_id']

        if 'category_id' in data:
            if data['category_id'] and not Category.query.get(data['category_id']):
                raise AppError('Category not found', 404)
            task.category_id = data['category_id']

        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').replace(tzinfo=timezone.utc)
                except ValueError:
                    raise AppError('Invalid date format')
            else:
                task.due_date = None

        if 'tags' in data:
            tags = data['tags']
            task.tags = ','.join(tags) if isinstance(tags, list) else tags

        task.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        logger.info("Task updated: %d", task.id)
        return task.to_dict()

    def delete(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            raise AppError('Task not found', 404)

        db.session.delete(task)
        db.session.commit()
        logger.info("Task deleted: %d", task_id)
        return {'message': 'Task deleted successfully'}

    def search(self, filters):
        query = Task.query

        q = filters.get('q', '')
        if q:
            query = query.filter(
                db.or_(
                    Task.title.like(f'%{q}%'),
                    Task.description.like(f'%{q}%')
                )
            )

        status = filters.get('status', '')
        if status:
            query = query.filter(Task.status == status)

        priority = filters.get('priority', '')
        if priority:
            query = query.filter(Task.priority == int(priority))

        user_id = filters.get('user_id', '')
        if user_id:
            query = query.filter(Task.user_id == int(user_id))

        tasks = query.all()
        return [t.to_dict() for t in tasks]

    def get_stats(self):
        total = Task.query.count()
        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        done = Task.query.filter_by(status='done').count()
        cancelled = Task.query.filter_by(status='cancelled').count()

        overdue_count = sum(1 for t in Task.query.all() if t.is_overdue())

        return {
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'done': done,
            'cancelled': cancelled,
            'overdue': overdue_count,
            'completion_rate': round((done / total) * 100, 2) if total > 0 else 0,
        }

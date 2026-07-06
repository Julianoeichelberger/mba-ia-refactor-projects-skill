import logging

from models.database import db
from models.task import Task
from models.category import Category
from middlewares.error_handler import AppError

logger = logging.getLogger(__name__)


class CategoryController:

    def get_all(self):
        categories = Category.query.all()
        result = []
        for c in categories:
            data = c.to_dict()
            data['task_count'] = Task.query.filter_by(category_id=c.id).count()
            result.append(data)
        return result

    def create(self, data):
        if not data:
            raise AppError('Invalid data')

        name = data.get('name')
        if not name:
            raise AppError('Name is required')

        category = Category()
        category.name = name
        category.description = data.get('description', '')
        category.color = data.get('color', '#000000')

        db.session.add(category)
        db.session.commit()
        logger.info("Category created: %d - %s", category.id, category.name)
        return category.to_dict()

    def update(self, cat_id, data):
        cat = Category.query.get(cat_id)
        if not cat:
            raise AppError('Category not found', 404)

        if 'name' in data:
            cat.name = data['name']
        if 'description' in data:
            cat.description = data['description']
        if 'color' in data:
            cat.color = data['color']

        db.session.commit()
        return cat.to_dict()

    def delete(self, cat_id):
        cat = Category.query.get(cat_id)
        if not cat:
            raise AppError('Category not found', 404)

        db.session.delete(cat)
        db.session.commit()
        logger.info("Category deleted: %d", cat_id)
        return {'message': 'Category deleted'}

import logging
import smtplib
from datetime import datetime, timezone

from config.settings import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self.notifications = []

    def send_email(self, to, subject, body):
        try:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(SMTP_USER, to, message)
            server.quit()
            logger.info("Email sent to %s", to)
            return True
        except Exception:
            logger.exception("Failed to send email to %s", to)
            return False

    def notify_task_assigned(self, user, task):
        subject = f"New task assigned: {task.title}"
        body = f"Hello {user.name},\n\nThe task '{task.title}' has been assigned to you.\n\nPriority: {task.priority}\nStatus: {task.status}"
        self.send_email(user.email, subject, body)
        self.notifications.append({
            'type': 'task_assigned',
            'user_id': user.id,
            'task_id': task.id,
            'timestamp': datetime.now(timezone.utc),
        })

    def notify_task_overdue(self, user, task):
        subject = f"Task overdue: {task.title}"
        body = f"Hello {user.name},\n\nThe task '{task.title}' is overdue!\n\nDue date: {task.due_date}"
        self.send_email(user.email, subject, body)

    def get_notifications(self, user_id):
        return [n for n in self.notifications if n['user_id'] == user_id]

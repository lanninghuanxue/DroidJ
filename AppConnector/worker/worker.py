from __future__ import absolute_import

from celery import Celery

workerApp = Celery('worker',
             broker='amqp://mqs',
             backend='amqp://mqs',
             include=['worker.tasks'])

# Optional configuration, see the application user guide.
workerApp.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    workerApp.start()
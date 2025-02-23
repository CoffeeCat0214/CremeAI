from services.task_service import celery_app

if __name__ == '__main__':
    celery_app.start() 
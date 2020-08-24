docker run -itd --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
celery worker -A app.services.tasks -l debug -E \
flower -A app.services.tasks -l debug -E
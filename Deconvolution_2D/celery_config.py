import os

broker_url = os.environ.get("CELERY_BROKER")
result_backend = 'rpc://'
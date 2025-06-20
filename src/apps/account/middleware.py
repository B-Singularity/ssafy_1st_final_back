import logging
import uuid
from threading import local

from django.contrib.auth.models import AnonymousUser

_thread_locals = local()
logger = logging.getLogger(__name__)

def get_current_request_id():
    return getattr(_thread_locals, "request_id", None)

def get_current_user():
    return getattr(_thread_locals, "user", None)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        _thread_locals.request_id = request_id

        if request.user.is_authenticated:
            _thread_locals.user = request.user
        else:
            _thread_locals.user = None

        logger.info(f"Request started: {request.method} {request.path}")

        response = self.get_response(request)

        logger.info(f"Request finished: {response.status_code}")

        del _thread_locals.request_id
        if hasattr(_thread_locals, "user"):
            del _thread_locals.user

        return response
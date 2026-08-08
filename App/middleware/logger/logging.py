import datetime
import json
import sys
import logging

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        for key in ("method", "path", "status_code", "client", "user_id", "email"):
            if hasattr(record, key):
                log_record[key] = getattr(record, key)

        return json.dumps(log_record, default=str)


def setup_auth_logging():
    logger = logging.getLogger("auth")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    return logger

#status code loger or any information
logger = logging.getLogger(__name__)
auth_logger = setup_auth_logging()


async def log_auth_requests(request, call_next):
    if not request.url.path.startswith("/auth"):
        return await call_next(request)

    extra = {
        "method": request.method,
        "path": request.url.path,
        "client": request.client.host if request.client else None,
    }

    try:
        response = await call_next(request)
    except Exception:
        auth_logger.exception("auth_request_failed", extra={**extra, "status_code": 500})
        raise

    auth_logger.info("auth_request", extra={**extra, "status_code": response.status_code})
    return response

import time
import logging
from functools import wraps


def retry(
    retries: int = 3,
    delay: int = 2,
    backoff: int = 2,
    logger: logging.Logger = None
):
    """
    Decorador de reintentos con backoff exponencial.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _retries = retries
            _delay = delay

            while _retries > 0:
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    _retries -= 1

                    if _retries == 0:
                        raise

                    if logger:
                        logger.warning(
                            f"Retrying {func.__name__} in {_delay}s... Error: {str(e)}"
                        )

                    time.sleep(_delay)
                    _delay *= backoff

        return wrapper

    return decorator

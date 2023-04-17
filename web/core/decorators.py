import time
from functools import wraps

def timing_decorator(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = view_func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Загрузка страницы заняла: {elapsed_time:.2f} секунд")
        return response
    return wrapper
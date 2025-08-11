import time
import functools


def cache(timeout: int, *lru_args, **lru_kwargs):
    """
    缓存装饰器，用于缓存函数的返回值，缓存时间为 timeout 秒
    :param timeout: 缓存时间，单位为秒
    :param lru_args: lru_cache 的参数
    :param lru_kwargs: lru_cache 的参数
    :return: 装饰器
    """

    def wrapper_cache(func):
        func = functools.lru_cache(*lru_args, **lru_kwargs)(func)
        func.delta = timeout
        func.expiration = time.monotonic() + func.delta

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if time.monotonic() >= func.expiration:
                func.cache_clear()
                func.expiration = time.monotonic() + func.delta
            return func(*args, **kwargs)

        wrapped_func.cache_info = func.cache_info
        wrapped_func.cache_clear = func.cache_clear
        return wrapped_func

    return wrapper_cache
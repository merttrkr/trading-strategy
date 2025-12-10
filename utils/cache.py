import os
import pickle
import time
import functools
import hashlib
from typing import Any, Callable, Optional

class TTLCache:
    """Time-To-Live (TTL) Cache implementation using file storage."""

    def __init__(self, cache_dir: str = ".cache", ttl_seconds: int = 3600):
        """Initializes the cache.

        Args:
            cache_dir: Directory to store cache files.
            ttl_seconds: Time to live in seconds.
        """
        self.cache_dir = cache_dir
        self.ttl_seconds = ttl_seconds
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def _get_cache_path(self, key: str) -> str:
        """Generates the file path for a cache key."""
        return os.path.join(self.cache_dir, f"{key}.pickle")

    def get(self, key: str) -> Optional[Any]:
        """Retrieves a value from the cache if valid.

        Args:
            key: The cache key.

        Returns:
            The cached value or None if not found or expired.
        """
        path = self._get_cache_path(key)
        if not os.path.exists(path):
            return None

        # Check TTL
        mtime = os.path.getmtime(path)
        if time.time() - mtime > self.ttl_seconds:
            return None

        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            return None

    def set(self, key: str, value: Any) -> None:
        """Sets a value in the cache.

        Args:
            key: The cache key.
            value: The value to cache.
        """
        path = self._get_cache_path(key)
        with open(path, "wb") as f:
            pickle.dump(value, f)

def cached(ttl_seconds: int = 3600, cache_dir: str = ".cache"):
    """Decorator to cache function results.

    Args:
        ttl_seconds: Time to live in seconds.
        cache_dir: Directory to store cache files.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check for skip cache flag
            if kwargs.pop('_skip_cache', False):
                return func(*args, **kwargs)

            # Generate cache key
            # We use the function name and arguments to generate a unique key
            key_parts = [func.__module__, func.__qualname__]
            key_parts.extend([str(arg) for arg in args])
            key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
            key_string = "|".join(key_parts)
            key = hashlib.md5(key_string.encode('utf-8')).hexdigest()

            cache = TTLCache(cache_dir, ttl_seconds)
            result = cache.get(key)

            if result is not None:
                return result

            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        return wrapper
    return decorator

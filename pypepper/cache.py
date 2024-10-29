# pypepper/cache.py


def connect_cache(host="localhost", port=6379):
    import redis

    """Connect to a Redis cache instance."""
    return redis.Redis(host=host, port=port)

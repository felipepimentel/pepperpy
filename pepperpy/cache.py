# pypepper/cache.py


def connect_cache(host="localhost", port=6379):
    import redis

    return redis.Redis(host=host, port=port)

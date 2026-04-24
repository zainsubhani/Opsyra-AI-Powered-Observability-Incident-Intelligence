import json

import redis

from opsyra_common.config import get_shared_settings


def get_redis_client() -> redis.Redis | None:
    settings = get_shared_settings()
    if not settings.redis_url:
        return None
    return redis.Redis.from_url(settings.redis_url, decode_responses=True)


def publish_event(stream_name: str, payload: dict[str, str]) -> bool:
    client = get_redis_client()
    if client is None:
        return False
    client.xadd(stream_name, {"payload": json.dumps(payload)})
    return True

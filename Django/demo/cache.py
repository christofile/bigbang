# -*- coding: utf-8 -*-
from models import User
from utils import config
from utils import common
from exception import IllegalArgumentError
import redis
import json

# 获取redis配置
_redis_server_ip = config.get_config('REDIS_SERVER_IP', )
_redis_server_port = config.get_config('REDIS_SERVER_PORT', )

if not _redis_server_ip or not _redis_server_port:
    raise IllegalArgumentError("redis config is invalid!")


#redis实例
_redisIns = redis.StrictRedis(host=_redis_server_ip, port=_redis_server_port, db=0)

def _get(key):
    return _redisIns.get(key)  # if key not exist, return None


def _set(key, value, timeout=-1):
    ret = _redisIns.set(key, value)
    if timeout and timeout > 0:
        _redisIns.expire(key, timeout)
    return ret


# hash type
def _hmset(key, mapping, timeout=-1):
    ret = _redisIns.hmset(key, mapping)
    if timeout and timeout > 0:
        _redisIns.expire(key, timeout)
    return ret


# if key not exist, return empty dict {}
def _hgetall(key):
    return _redisIns.hgetall(key)


# 设置用户登录session
def set_login_session(id, data):
    if not id:
        raise IllegalArgumentError("session_id can't be None!")

    key = 'login-session:' + str(id)
    return _hmset(key, data)

# 获取用户登录session
def get_login_session(id):
    if not id:
        raise IllegalArgumentError("session_id can't be None!")

    key = 'login-session:' + str(id)
    return _hgetall(key)





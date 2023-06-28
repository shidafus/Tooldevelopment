import redis
import re
from config.settings import REDIS

# 本地连接，创建数据库连接对象
r = redis.Redis(host=REDIS.get('host'), port=REDIS.get('port'),
                db=REDIS.get('database'), password=REDIS.get('password'))
pattern = re.compile("^loginToken", re.I)
data = [elem for elem in r.keys('*') if pattern.search(elem.decode('utf-8'))]
_ = [{print(res, end=': '), print(r.get(res))} for res in data]

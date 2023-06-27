from mong import MongoHelper
import re

mongo_helper = MongoHelper()


# 列出集合
def show_jihe(list):
    for i in list:
        print(i)
    print("-------------------------------------")


# 查看单个集合的列表字段,或第一行数据
def show_dbsorkeys(connections_name: str):
    for k, v in mongo_helper.fetch_one(connections_name).items():
        print(f'{k}: {v}')


# 查询匹配更多数据
def show_all_dbs(connections_name, filters=None):
    data = mongo_helper.fetch_all(connections_name, filters)
    _ = [print(i) for i in data]
    print(f'一共有{len(data)}条数据')


if __name__ == '__main__':
    list = mongo_helper.get_connections()

    # 查看该数据库所有集合
    show_jihe(list)

    # 查看单个集合的列表字段
    show_dbsorkeys('tk_client_wait_log')

    # 更具上面给出的字段 进行查询数据
    # 定义查询条件默认为空     $lt 小于  $lte 小于等于    $gt大于  $gte 大于等于  $ln  在之中   $nin 不在之中
    filters = {'username': {'$in': ['test111', 'test222']}}
    show_all_dbs('tk_client_wait_log',filters)



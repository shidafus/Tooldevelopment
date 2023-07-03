from mong import MongoHelper

mongo_helper = MongoHelper()


# 列出集合
def show_jive(lists):
    for i in lists:
        print(i)
    print("-------------------------------------")


# 查看单个集合的列表字段,或第一行数据
def show_donkeys(connections_name: str):
    for k, v in mongo_helper.fetch_one(connections_name).items():
        print(f'{k}: {v}')


# 查询匹配更多数据
def show_all_dbs(connections_name, filters=None):
    data = mongo_helper.fetch_all(connections_name, filters)
    _ = [print(i) for i in data]
    print(f'一共有{len(data)}条数据')


if __name__ == '__main__':
    # 查看该数据库所有集合
    show_jive(mongo_helper.get_connections())

    # 查看单个集合的列表字段
    # show_donkeys('user')

    # # 更具上面给出的字段 进行查询数据
    # # 定义查询条件默认为空     $lt 小于  $lte 小于等于    $gt大于  $gte 大于等于  $ln  在之中   $nin 不在之中
    filterer = {'_id': '10170429' }
    show_all_dbs('user', filterer)

import requests
import json

message = "from flask imposdfasdfasdfsdf, jsonify"

def send_dingding_msg():
    url = "https://oapi.dingtalk.com/robot/send?access_token=45fb16618de809aa301caae929c8e1eac16e3813ec125413563e38810fe43337"
    headers = {"Content-Type": "application/json;charset=utf-8"}

    data = {
        "msgtype": "text",
        "text": {
            # 消息内容部分（必填）
            "content": message
        },
        # 可选项：@某个用户
        # "at":{
        # "atMobiles": [],
        # "isAtAll": True,
        # },
    }

    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r)


send_dingding_msg()
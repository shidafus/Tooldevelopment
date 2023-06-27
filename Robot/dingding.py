import requests
import json

message = """from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['GET'])
def do_run():
    command = request.args.get('command')
    
    if not command:
        return jsonify({"message": "命令不能为空"}), 400
    
    # 使用subprocess模块运行命令并返回结果字符串到调用者 
    try:
        result_bytes = subprocess.check_output(command.split())
        result_str = result_bytes.decode("utf8")
        
        return jsonify({"result": result_str})
    except subprocess.CalledProcessError as e:
        return jsonify({"message": "命令执行失败", "error": str(e)}), 400

"""

def send_dingding_msg():
    url = "https://oapi.dingtalk.com/robot/send?access_token=45fb16618de809aa301caae929c8e1eac16e3813ec125413563e38810fe43337&timestamp=SEC1cf0ec239b322e4df1d3db644762081749873c6d28cbf34a562669ef0d4ec487"
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


send_dingding_msg()
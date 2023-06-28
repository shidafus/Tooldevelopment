# -- coding:UTF-8 --


import requests


class IMUser:

    def __init__(self, phone, password, url):
        self.phone = phone
        self.password = password
        try:
            response = requests.get(url, timeout=10)
        except:
            self.api = "http://118.107.45.190:8084/api/v1.0/link/getCheckDomainList"
            return

        self.api = response.json()['data']['apiUrlList'][0]["url"]
        print(response.json()['data']['apiUrlList'][0]["url"])

    def gettoken(self):
        json_data = {
            'areaCode': 86,
            'phone': self.phone,
            'passWord': self.password,
        }
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh',
            'request-startTime': '1678347631986',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'each-chat/0.0.51 Chrome/87.0.4280.141 Electron/11.5.0 Safari/537.36',
            'Client-Type': 'Pc',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
        }
        try:
            response = requests.post(self.api + 'api/v1.0/member/userLogin', headers=headers,
                                     json=json_data, timeout=10)
        except:
            return ''

        print(response.json()["data"]["oAuth"]["token"])
        return response.json()["data"]["oAuth"]["token"]

    def do_locker(self, user_key, tokens):

        json_data = {
            "lockReason": "该账号因涉嫌传播/暴力/非法营销等违法内容被执行封号,详情请阅读账号使用规范.",
            "toUserKey": user_key
        }
        headers = {
            "accessToken": tokens,
            'Accept': 'application/json, text/plain, */*',
            'Client-Type': 'Pc',
            'Accept-Language': 'zh',
        }
        try:
            response = requests.post(self.api + 'api/v1.0/security/lockUser', headers=headers,
                                     json=json_data, timeout=10)
        except:
            print(user_key + " 请求接口失败")
            return

        if response.json()["resultCode"] == 200 and response.json()["resultMsg"] == "":
            print(user_key + " ok")
        return

    def do_unlocker(self, user_key, tokens):

        json_data = {
            "toUserKey": user_key
        }
        headers = {
            "accessToken": tokens,
            'Accept': 'application/json, text/plain, */*',
            'Client-Type': 'Pc',
            'Accept-Language': 'zh',
        }
        try:
            response = requests.post(self.api + 'api/v1.0/security/unlockUser', headers=headers,
                                     json=json_data, timeout=10)
        except:
            print(user_key + " 请求接口失败")
            return

        if response.json()["resultCode"] == 200 and response.json()["resultMsg"] == "":
            print(user_key + " ok")
        return


if __name__ == '__main__':
    # with open('msg/' + sys.argv[2]) as f:
    #     msg = f.read()
    # if msg == '':
    #     print(u"输入内容为空")
    # json_msg = json.loads(msg)
    # if json_msg["text"] == '':
    #     print(u"输入内容为空")
    #
    # text = json_msg["text"]
    # text = "Exid_MTAwMDAwMTE=\n"
    p = "13666666666"
    # phone = "13700137004"
    pw = "f8232a4936a98c5fb4e4bab9e076d3ae"
    # IM = IMUser(phone, password, 'http://192.168.11.100:8001/api/v1.0/link/getCheckDomainList')
    IM = IMUser(p, pw, 'https://config500.oss-cn-hongkong.aliyuncs.com/api/v1.0/config/get')
    token = IM.gettoken()
    # if token == "":
    #     print(u"获取token失败")
    #     exit(0)
    #
    # for i in text.split("\n"):
    #     if i == "":
    #         continue
    #     lock_user = str(i).strip()
    #     if sys.argv[1] == "lock":
    #         IM.do_lockuser(lock_user, token)
    #     elif sys.argv[1] == "unlock":
    #         IM.do_unlockuser(lock_user, token)

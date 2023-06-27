import http, requests, os
import json
from hashlib import md5


class request():

    # 初始化
    def __init__(self, username, password, url):

        self.token = None
        self.username = username
        self.password = password
        self.url = url

    # 得到用户信息 并return 结果
    def get_user_information(self):
        json_data = {}
        headers = {
            "accessToken": self.token,
        }
        url = 'http://192.168.11.100:8001/api/v1.0/user/get'

        response = requests.get(url, headers=headers, json=json_data, timeout=10)

        return response.json()

    # 获取token 并return
    def get_token(self):
        json_data = {
            'areaCode': 86,
            'phone': self.username,
            'passWord': self.password,
        }
        headers = {

            'Accept-Language': 'zh',
            'Client-Type': 'Pc',

        }

        try:
            response = requests.post(self.url, headers=headers, json=json_data, timeout=10)
            # print(response.json())
        except:
            return print("有问题啊")
        self.token = response.json()["data"]["oAuth"]["token"]
        print(self.token)
        # return response.json()["data"]["oAuth"]["token"]

    # 上传文件
    def post_file(self,file_path):

        fileobject = {

            'type': (None, '6', None),
            'orgType': (None, 'B', None),
            'file': (os.path.basename(file_path), open(file_path, 'rb'),
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }

        headers = {
            # 'Content-type': 'multipart/form-data;boundary=----WebKitFormBoundary8yG5u2HKOJ3lSXZM',   # 该值会在请求的时候自动加上
            'accessToken': self.token
        }

        url = "http://192.168.11.100:8009/api/v1.0/upload/uploadHead"
        response = requests.post(url, files=fileobject, headers=headers)
        if response.status_code == 200:
            print("Upload success!")
        else:
            print(f"Error:{response}")

    # 用户密码加密
    def cryptographic_encryption(self):
        m = md5()
        m.update(self.password.encode())
        self.password = m.hexdigest()


if __name__ == '__main__':
    # username = '13535325758'
    # password = '123456'
    username = '13535325758'
    password = '123456'
    url = "http://192.168.11.100:8001/api/v1.0/member/userLogin"
    # url = "http://192.168.101.101:8084/api/v1.0/member/userLogin"

    qinqiu = request(username, password, url)
    qinqiu.cryptographic_encryption()
    qinqiu.get_token()
    qinqiu.post_file(r'C:\Users\zhoujiahao\Desktop\MouseWithoutBorders\d0e09bdc26164bc5a67c4c376f6d218f.jpg')


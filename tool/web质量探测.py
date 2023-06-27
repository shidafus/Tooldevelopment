import pycurl
import os, sys
import time

"""
c = pycurl.Curl()

c.setopt(pycurl.CONNECTTIMEOUT, 5)   # 连接的等待时间, 设置为0 则不等待

c.setopt(pycurl.TIMEOUT, 5)          # 请求超时时间

c.setopt(pycurl.NOPROGRESS, 0)       # 是否屏蔽下载进度条, 非0 则屏蔽

c.setopt(pycurl.MAXREDIRS, 5)        # 指定HTTP重定向的最大数

c.setopt(pycurl.FORBID_REUSE, 1)     # 完成交互后强制断开连接,不重用

c.setopt(pycurl.FRESH_CONNECT, 1)    # 强制获取新的连接,即代替缓存中的连接

c.setopt(pycurl.DNS_CACHE_TIMEOUT, 60)  # 设置保存DNS信息的时间,默认为120秒

c.setopt(pycurl.URL, "http://www.baidu.com")  # 指定请求的URL

c.setopt(pycurl.USERAGENT,
         "Mozilla/5.2  (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50324)")

c.setopt(pycurl.HEADERFUNCTION, getheader)    # 将返回的HTTP HEADER 定向到回调函数  getheader

c.setopt(pycurl.WRITEFUNCTION, getbody)   # 将返回的内容定向到回调函数getbody

c.setopt(pycurl.WRITEHEADER, fileobj)      # 将返回的HTTP HEADER 定向到fileobj

c.setopt(pycurl.WRITEDATA, fileobj)        # 将返回的HTML内容定向到fileobj文件


c.getinfo(pycurl.HTTP_CODE)         # 返回的HTTP状态码

c.getinfo(pycurl.TOTAL_TIME)        # 传输结束所兄啊好的总时间

c.getinfo(pycurl.NAMELOOKUP_TIME)   # DNS解析所消耗的时间

c.getinfo(pycurl.PRETRANSFER_TIME)  # 从建立连接到准备传输所消耗的时间

c.getinfo(pycurl.STARTTRANSFER_TIME)  # 从建立连接到准备传输所消耗的时间

c.getinfo(pycurl.REDIRECT_TIME)       # 重定向所消耗的时间

c.getinfo(pycurl.SIZE_UPLOAD)         # 上传数据包大小

c.getinfo(pycurl.SIZE_DOWNLOAD)        # 下载数据包大小

c.getinfo(pycurl.SPEED_DOWNLOAD)        # 下载的平均速度

c.getinfo(pycurl.SPEED_UPLOAD)          # 平均上传速度

c.getinfo(pycurl.HEADER_SIZE)           # HTTP 头部大小 

"""

def create_url(URL):
    # URL = "https://www.baidu.com"
    c = pycurl.Curl()  # 创建一个Curl对象

    c.setopt(pycurl.URL, URL)  # 定义请求的URL常量

    c.setopt(pycurl.TIMEOUT, 5)  # 定义请求超时时间

    c.setopt(pycurl.NOPROGRESS, 1)  # 屏蔽下载进度条

    c.setopt(pycurl.FORBID_REUSE, 1)  # 完成交互后强制断开连接,不重用

    c.setopt(pycurl.MAXREDIRS, 3)  # 指定HTTP重定向的最大数为 3

    c.setopt(pycurl.FOLLOWLOCATION, 3)  # 设置跟随最大次重定向的 次数

    c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)  # 设置保存DNS信息的时间为30秒


    # 创建一个文件对象,以"web" 的方式打开,用来存储返回的HTTP头部及页面内容

    indexfile = open(os.path.dirname(os.path.realpath(__file__)) + "/content.txt", "wb")

    c.setopt(pycurl.WRITEHEADER, indexfile)  # 将返回的HTTP  HEADER定向到 indexfile文件对象

    c.setopt(pycurl.WRITEDATA, indexfile)  # 将返回的HTML内容定向到 indexfile 文件对象
    return c, indexfile

def submit_request(c, indexfile):
    try:
        c.perform()  # 提交请求
        return c
    except Exception as error:
        print(f"connecion error:n {error}")
        indexfile.close()
        c.close()
        sys.exit()

def fetch_request_data(c, indexfile):
    HTTP_CODE = c.getinfo(c.HTTP_CODE)  # 获取HTTP状态码
    NAMELOOKUP_TIME = c.getinfo(c.NAMELOOKUP_TIME)  # 获取DNS解析时间
    CONNEXT_TIME = c.getinfo(c.CONNECT_TIME)  # 获取建立连接时间
    PRETRANSFER_TIME = c.getinfo(c.PRETRANSFER_TIME)  # 获取从建立连接到准备传输所消耗的时间
    STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME)  # 获取从建立连接到传输开始消耗的时间
    TOTAL_TIME = c.getinfo(c.TOTAL_TIME)  # 获取传输的总时间
    SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD)  # 获取下载数据包大小
    HEADER_SIZE = c.getinfo(c.HEADER_SIZE)  # 获取HTTP头部大小
    SPEED_DOWNLOAD = c.getinfo(c.SPEED_DOWNLOAD)  # 获取平均下载速度

    # 打印相关数据
    print("HTTP状态码: %s" % (HTTP_CODE))
    print("DNS解析时间: %.3f ms" % (NAMELOOKUP_TIME))
    print("重定向消耗时间: %.3f ms" % (pycurl.REDIRECT_TIME))
    print("建立连接时间: %.3f ms" % (CONNEXT_TIME))
    print("准备传输所消耗的时间: %.3f ms" % (PRETRANSFER_TIME))
    print("传输开始消耗的时间: %.3f ms" % (STARTTRANSFER_TIME))
    print("传输的总时间: %.3f ms" % (TOTAL_TIME))
    print("下载数据包大小: %d bytes/s" % (SIZE_DOWNLOAD))
    print("HTTP头部大小: %d byte" % (HEADER_SIZE))
    print("平均下载速度: %d byte/s" % (SPEED_DOWNLOAD))

    # 关闭文件及 Curl对象
    indexfile.close()
    c.close()


if __name__ == "__main__":
    c, indexfile = create_url("http://www.baidu.com")
    c = submit_request(c, indexfile)
    fetch_request_data(c, indexfile)




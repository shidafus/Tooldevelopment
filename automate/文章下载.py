import requests
from html2text import HTML2Text


def download_article(url):
    # 发送GET请求获取文章内容
    response = requests.get(url)

    if response.status_code == 200:
        # 将收到的HTML转换为Markdown格式文本
        converter = HTML2Text()
        markdown_text = converter.handle(response.text)
        # 将内容保存到文件
        with open('file.md', 'w', encoding='utf-8') as f:
            f.write(markdown_text)
    else:
        print("文章获取失败!")


# 调用函数下载博客文章
urls = "https://www.cnblogs.com/Nephalem-262667641/p/17310765.html#4.1-re.match"

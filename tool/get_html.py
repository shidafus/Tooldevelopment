import requests

url = "https://www.csdn.net"
headers = {
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.100.4811.0 Safari/537.36"
}

res = requests.get(url, 'lxml', headers=headers)
html = res.text.encode(res.encoding).decode()
print(res.encoding)

# with open('www.html', mode="w", encoding='utf8') as file:
#     file.write(html)
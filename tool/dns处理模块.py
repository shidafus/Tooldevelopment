import dns.resolver
from pip._vendor.distlib.compat import raw_input

"""
1. A 记录（Address Record）：将域名解析为 IPv4 地址。A 记录是最常用的 DNS 记录类型，它将域名映射到一个 IPv4 地址，当用户在浏览器中输入域名时，浏览器会向 DNS 服务器查询该域名的 A 记录，获取域名对应的 IP 地址，然后访问该 IP 地址的服务器。

2. AAAA 记录（IPv6 Address Record）：将域名解析为 IPv6 地址。AAA 记录与 A 记录功能相同，只是将域名解析为 IPv6 地址。

3. CNAME 记录（Canonical Name Record）：将域名解析为另一个域名。CNAME 记录允许将一个域名指向另一个域名，这样，当用户访问第一个域名时，DNS 服务器会返回第二个域名的 IP 地址，从而实现域名重定向。

4. MX 记录（Mail Exchange Record）：指定邮件服务器的域名和优先级。MX 记录指定处理特定域名的邮件服务器，当用户发送邮件时，邮件客户端会查询该域名的 MX 记录，找到处理该域名邮件的服务器。

5. NS 记录（Name Server Record）：指定域名服务器的地址。NS 记录指定处理特定域名的 DNS 服务器，当用户查询该域名的 DNS 信息时，DNS 服务器会返回该域名的 NS 记录，告诉用户应该向哪个 DNS 服务器查询该域名的 A 记录或其他记录类型。

6. PTR 记录（Pointer Record）：将 IP 地址解析为域名。PTR 记录是 A 记录的反向解析，它将 IP 地址解析为对应的域名，当用户查询某个 IP 地址的域名时，DNS 服务器会返回该 IP 地址对应的 PTR 记录。

7. SOA 记录（Start of Authority Record）：指定域名的授权域名服务器、管理员邮箱、序列号等。SOA 记录是每个域名区域文件中必须包含的记录类型，它包含域名的授权域名服务器、域名管理员的邮箱地址、序列号等信息。

8. SRV 记录（Service Record）：指定提供特定服务的服务器的地址和端口号。SRV 记录用于指定提供特定服务的服务器的地址和端口号，例如，当用户访问某个域名的 Jabber 服务时，DNS 服务器会返回该域名的 SRV 记录，告诉用户应该连接哪个服务器的哪个端口。

9. TXT 记录（Text Record）：提供任意文本信息。TXT 记录可以用于提供任意文本信息，例如，用于验证域名所有权、提供 DKIM 签名等。
"""

# 获取域名的A记录
def A_jilu():
    domain = input('Please input a domain: ')
    A = dns.resolver.resolve(domain, 'A')

    for i in A.response.answer:
        for j in i.items:
            if j.rdtype == dns.rdatatype.CNAME:
                pass
            else:
                print(j.address)



def CNAME_jilu():
    domain = input('Please input a domain: ')
    CNAME = dns.resolver.resolve(domain, 'CNAME')

    for i in CNAME.response.answer:
        for j in i.items:
            print(j.target)


# 获取域名的NS记录
def NS_jilu():
    domain = input('Please input a domain: ')
    NS = dns.resolver.resolve(domain, 'NS')
    for i in NS.response.answer:
        for j in i.items:
            print(j.target)


# 查询 MX 记录
def MX_jilu():
    domain = input('Please input a domain: ')
    MX = dns.resolver.resolve(domain, 'MX')
    for i in MX:
        print(i.exchange, 'has preference', i.preference)

A_jilu()
import dns.resolver
import http.client


iplist= []

appdomain = 'wishufu.wismall.com'

def get_iplist(domain=""):
    try:
        A = dns.resolver.resolve(domain, 'A')

    except Exception as e:
        print("dns resolver error:"+str(e))
        return

    for i in A.response.answer:
        for j in i.items:
            if j.rdtype == dns.rdatatype.CNAME:
                pass
            else:
                iplist.append(j.address)
    return True

def checkip(ip):
    checkurl = ip + ":80"
    http.client.socket.setdefaulttimeout(5)
    conn = http.client.HTTPConnection(checkurl)

    try:
        conn.request("GET", "/", headers= {"Host": appdomain})

        r = conn.getresponse()
        if r.status == 200:
            print(ip + " ok")
        else:
            print(ip + " Error")
    except Exception as e:
        print(ip + " Error")
    finally:
        conn.close()

if __name__ == "__main__":
    if get_iplist(appdomain) and len(iplist)>0:
        for ip in iplist:
            checkip(ip)
    else:
        print("dns resolver error!")
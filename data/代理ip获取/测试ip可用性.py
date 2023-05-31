import urllib.request


def hymh_test(ip):
    url = 'http://api.binjie.fun/'
    try:
        proxy_support = urllib.request.ProxyHandler({'http': ip})
        # 接着创建一个包含代理IP的opener
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        # 查看IP地址是否改变
        response = urllib.request.urlopen(url, timeout=4)
        html = response.read().decode('utf-8')
    except Exception as e:
        return e
    return "<html><head>" in html

def test_from_txt():
    good_ips = []
    with open('ips.txt', encoding='utf8') as f:
        ips = f.readlines()
    for index, ip in enumerate(ips):
        ip = ip.strip()
        res = hymh_test(ip)
        print(index, ip, res)
        if res == True:
            good_ips.append(ip + "\n")
    with open('goodIps.txt', 'w') as f:
        f.writelines(good_ips)

if __name__ == '__main__':
    # print(hymh_test('1.2.2.3:555'))
    test_from_txt()
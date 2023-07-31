import random
import urllib.request

import eventlet
import eventlet.hubs.epolls
import eventlet.hubs.kqueue
import eventlet.hubs.selects
import requests
import dns
import dns.asyncbackend
import dns.asyncquery
import dns.asyncresolver
import dns.dnssec
import dns.e164
import dns.edns
import dns.entropy
import dns.exception
import dns.flags
import dns.immutable
import dns.inet
import dns.ipv4
import dns.ipv6
import dns.message
import dns.name
import dns.namedict
import dns.node
import dns.opcode
import dns.query
import dns.rcode
import dns.rdata
import dns.rdataclass
import dns.rdataset
import dns.rdatatype
import dns.tsigkeyring
import dns.ttl
import dns.rdtypes
import dns.update
import dns.version
import dns.versioned
import dns.wire
import dns.xfr
import dns.zone
import dns.zonefile

# 获取随机User_Agent伪装
import time
from bs4 import BeautifulSoup

eventlet.monkey_patch(time=True)

Version = "v1.."
print(Version)

global exits_ips
exits_ips = []


def getIpBy89ip(iplist=[], pages=5):
    """
    从89ip获取代理ip
    :param iplist: 当前已收集ip列表
    :param pages: 采集页数
    :return: ip列表
    """
    for page in range(1, pages + 1):
        print(f"=======================[89ip]ip--第{page}/{pages}页=======================")
        try:
            url = f'https://www.89ip.cn/index_{page}.html'
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req, timeout=10)
            ip_page = res.read().decode('utf8')
            soup = BeautifulSoup(ip_page, 'html.parser')
            trs = soup.select('tbody tr')
            iplist = checkIpExits(iplist, trs, 5)
            timeout(1)
        except Exception as e:
            print("89ip--获取ip失败，页码：", page, e)
            continue
    return iplist


UAs = [
    "Mozilla/5.0 (Linux; Android 10; ONEPLUS A5010 Build/QKQ1.191014.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/2954 MicroMessenger/8.0.27.2220(0x28001BA2) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 9; RVL-AL09 Build/HUAWEIRVL-AL09; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/1773 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 10; ONEPLUS A5010 Build/QKQ1.191014.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/6969 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x18001442) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 9; MI 6X Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220709 Mobile Safari/537.36 MMWEBID/2998 MicroMessenger/8.0.25.2200(0x28001953) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 10; YAL-AL00 Build/HUAWEIYAL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4255 MMWEBSDK/20220604 Mobile Safari/537.36 MMWEBID/7550 MicroMessenger/8.0.24.2180(0x28001837) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 12; SM-G9980 Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4309 MMWEBSDK/20220303 Mobile Safari/537.36 MMWEBID/4948 MicroMessenger/8.0.21.2120(0x280015F0) Process/toolsmp WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 10; ELS-AN00 Build/HUAWEIELS-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/4652 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 10; ELS-AN00 Build/HUAWEIELS-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36 MMWEBID/4652 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/5463 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.27(0x18001b34) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 11; MEIZU 18 Build/RKQ1.210715.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/8052 MicroMessenger/8.0.27.2220(0x28001B53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 12; PDPM00 Build/RKQ1.211103.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/3466 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 10; STK-AL00 Build/HUAWEISTK-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/788 MicroMessenger/8.0.27.2220(0x28001BDF) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 11; M2011K2C Build/RKQ1.200928.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220709 Mobile Safari/537.36 MMWEBID/3382 MicroMessenger/8.0.25.2200(0x28001953) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Build/RKQ1.201004.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/1079 MicroMessenger/8.0.27.2220(0x28001BCA) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 10; Redmi K30 5G Build/QKQ1.191222.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220505 Mobile Safari/537.36 MMWEBID/3224 MicroMessenger/8.0.23.2160(0x28001757) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 10; OXF-AN10 Build/HUAWEIOXF-AN10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/1579 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 10; HMA-AL00 Build/HUAWEIHMA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/4967 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 10; M2007J22C Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4309 MMWEBSDK/20220303 Mobile Safari/537.36 MMWEBID/1027 MicroMessenger/8.0.21.2120(0x280015F0) Process/toolsmp WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220709 Mobile Safari/537.36 MMWEBID/709 MicroMessenger/8.0.25.2200(0x28001953) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x18001442) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 11; MI 9 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4309 MMWEBSDK/20220709 Mobile Safari/537.36 MMWEBID/8824 MicroMessenger/8.0.25.2200(0x28001953) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.27(0x18001b34) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 10; YAL-AL10 Build/HUAWEIYAL-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/2803 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 10; YAL-AL00 Build/HUAWEIYAL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/6532 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML; like Gecko) Mobile/12F70 MicroMessenger/6.1.5 NetType/WIFI"]

# 禁用安全请求警告,当目标使用htpps时使用
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getIpBykdl(iplist=[], pages=5):
    """
    从快代理获取代理ip
    :param iplist: 当前已收集ip列表
    :param pages: 采集页数
    :return: ip列表
    """

    # proxy_support = urllib.request.ProxyHandler({'https': "127.0.0.1:8888"})
    # # 接着创建一个包含代理IP的opener
    # opener = urllib.request.build_opener(proxy_support)
    # urllib.request.install_opener(opener)
    for page in range(1, pages + 1):
        print(f"=======================[快代理]ip--第{page}/{pages}页=======================")
        try:
            url = f'https://www.kuaidaili.com/free/inha/{page}/'
            headers = {'User-Agent': random.choice(UAs), 'method': 'GET',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
            ip_page = requests.get(url, headers=headers, timeout=10, verify=False)
            ip_page = ip_page.text
            # print(ip_page)
            soup = BeautifulSoup(ip_page, 'html.parser')
            trs = soup.select('tbody tr')
            iplist = checkIpExits(iplist, trs, 7)
            timeout(1)
        except Exception as e:
            print("快代理--获取ip失败，页码：", page, e)
            continue
    return iplist


def getIpCommon(url_, mark, headers, iplist=[], pages=5):
    """
    获取代理ip
    :param url_: 网址链接
    :param mark: 备注
    :param headers:
    :param iplist: 当前已收集ip列表
    :param pages: 采集页数
    :return: ip列表
    """

    # proxy_support = urllib.request.ProxyHandler({'https': "127.0.0.1:8888"})
    # # 接着创建一个包含代理IP的opener
    # opener = urllib.request.build_opener(proxy_support)
    # urllib.request.install_opener(opener)
    for page in range(1, pages + 1):
        try:
            url = url_.replace("【page】", f'{page}')
            ip_page = requests.get(url, headers=headers, timeout=10, verify=False)
            ip_page = ip_page.text
            # print(ip_page)
            soup = BeautifulSoup(ip_page, 'html.parser')
            if mark == '66代理':
                print("66代理")
                trs = soup.select('#main table tr')[1:]
            else:
                trs = soup.select('tbody tr')
            # if len(trs) == 0:
            #     print("没有获取到trs，重新筛选")
            #     trs = soup.select('table tr')
            iplist = checkIpExits(iplist, trs, 7)
            print(f"=======================[{mark}]ip--第{page}/{pages}页=======================")
            timeout(1)
        except Exception as e:
            print(f"{mark}--获取ip失败，页码：{page}。错误信息：", e)
            continue
    return iplist


def checkIpExits(iplist, trs, tds_len):
    """
    检查ip是否已经存在
    :param iplist: 当前获取到的ip列表
    :param trs: bs4soup 解析的网页标签 tr
    :param tds_len: 正常情况下表格的列数 td
    :return:
    """
    global exits_ips
    for tr in trs:
        tds = tr.select("td")
        # assert len(tds) == tds_len
        ip = tds[0].text.strip() + ":" + tds[1].text.strip()
        # ip = '139.9.64.238:443'
        print(ip)
        if ip not in iplist and ip + '\n' not in exits_ips:
            iplist.append(ip)
        else:
            print('↑ 该IP已存在，跳过')
    return iplist


def hymh_test(ip):
    url = 'http://api.binjie.fun/'

    proxy_support = urllib.request.ProxyHandler({'http': ip})
    # 接着创建一个包含代理IP的opener
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    # 查看IP地址是否改变
    response = urllib.request.urlopen(url, timeout=4)
    html = response.read().decode('utf-8')
    return "<html><head>" in html


def timeout(_time):
    """
    超时限制
    :param _time:睡眠时间
    :return: 是否超时
    """
    with eventlet.Timeout(_time + 10, False):  # 设置超时间+10s
        time.sleep(_time)
        print('休眠结束')
        return False
    print('函数调用超时', _time)
    return True


import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.xxx.com"  # 设置服务器
mail_user = "xxx@xxx.com"  # 用户名
mail_pass = "xxx"  # 口令
sender = 'xxx@xxx.com'
receivers = ['xxx@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


def sendEmail(content):
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = "bhshare<yaokui_ltd@163.com>"  # 发送者
    message['To'] = "bhnw<1361453981@qq.com>"  # 接收者

    subject = '代理ip获取出错'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)


if __name__ == '__main__':
    pages_89ip = 5
    pages_kdl = 5
    time_sleep = 5
    pages_89ip = int(input('从【89ip】中提取的页数（默认5）：') or '5')
    pages_kdl = int(input('从【快代理】中提取的页数（默认5）：') or '5')
    pages_mifeng = int(input('从【蜜蜂代理】中提取的页数（默认5）：') or '5')
    pages_yun = int(input('从【云代理】中提取的页数（默认5）：') or '5')
    pages_66ip = int(input('从【66代理】中提取的页数（默认5）：') or '5')
    pages_kaixin1 = int(input('从【开心代理-高匿】中提取的页数（默认5）：') or '5')
    time_sleep = int(input('每次执行完休息的时间（默认5小时）：') or '5')
    time_sleep = time_sleep * 60 * 60
    try:
        import ctypes

        # 防止鼠标点击后cmd任务挂起
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
    except:
        print("=============不兼容ctypes，跳过============")

    errTimes = 0
    errText = ""
    # 索引值
    run_index = 1
    while True:
        new_ips = []
        try:
            print("\n\n错误次数：", errTimes)
            if errTimes > 10:
                print("错误超过10次，发送邮件，结束运行", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                # sendEmail(errText)
                break
            with open('ips.txt') as f:
                exits_ips = f.readlines()
            # exits_ips[-1] = exits_ips[-1] + '\n'
            print(f'当前已有ip数：{len(exits_ips)}')

            ua = random.choice(UAs)
            print("=======================开始获取[89代理]ip=======================")
            url = 'https://www.89ip.cn/index_【page】.html'
            headers = {'User-Agent': ua}
            new_ips = getIpCommon(url, mark='89代理', headers=headers, iplist=new_ips, pages=pages_89ip)
            # new_ips = getIpBy89ip(new_ips, pages_89ip)
            print("=======================开始获取[快代理]ip=======================")
            url = 'https://www.kuaidaili.com/free/inha/【page】/'
            headers = {'User-Agent': ua, 'method': 'GET',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
            new_ips = getIpCommon(url, mark='快代理', headers=headers, iplist=new_ips, pages=pages_kdl)
            # new_ips = getIpBykdl(new_ips, pages_kdl)
            print("=======================开始获取代理ip=======================")
            url = 'https://www.beesproxy.com/free/page/【page】'
            headers = {'User-Agent': ua}
            new_ips = getIpCommon(url, mark='蜜蜂代理', headers=headers, iplist=new_ips, pages=pages_mifeng)
            print("=======================开始获取代理ip=======================")
            url = 'http://www.ip3366.net/free/?stype=1&page=【page】'
            headers = {'User-Agent': ua}
            new_ips = getIpCommon(url, mark='云代理', headers=headers, iplist=new_ips, pages=pages_yun)
            print("=======================开始获取代理ip=======================")
            url = 'http://www.66ip.cn/【page】.html'
            headers = {'User-Agent': ua}
            new_ips = getIpCommon(url, mark='66代理', headers=headers, iplist=new_ips, pages=pages_66ip)
            print("=======================开始获取代理ip=======================")
            url = 'http://www.kxdaili.com/dailiip/1/【page】.html'
            headers = {'User-Agent': ua}
            new_ips = getIpCommon(url, mark='开心代理-高匿', headers=headers, iplist=new_ips, pages=pages_kaixin1)

            # 开始检测ip可用性
            print(f'本次共获取到ip数：{len(new_ips)}')
            print("=======================开始检测代理ip可用性=======================")
            good_ips = ""
            for index, ip in enumerate(new_ips):
                ip = ip.strip()
                try:
                    a = hymh_test(ip)
                    print(f'{index}/{len(new_ips)} ◆◆', a, ip)
                    if a == True:
                        good_ips += ip + "\n"
                except Exception as e:
                    print(f'{index}/{len(new_ips)}', e)
            print(f'本次获取到可用ip：\n{good_ips}')

            with open('ips.txt', 'a+') as f:
                f.write(good_ips)
            print(run_index, '文件写入成功。', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("\n\n=======================开始检测已有ip可用性=======================")
            good_ips = ""
            bad_ips = ""
            good_count = 0
            bad_count = 0
            new_ips = []
            with open("ips.txt") as f:
                new_ips.extend(f.readlines())
            with open("ips_err.txt") as f:
                new_ips.extend(f.readlines())
            for index, ip in enumerate(new_ips):
                ip = ip.strip()
                try:
                    a = hymh_test(ip)
                    print(f'{index}/{len(new_ips)} ◆◆', a, ip)
                    if a == True:
                        good_ips += ip + "\n"
                        good_count += 1
                        continue
                except Exception as e:
                    print(f'{index}/{len(new_ips)}', e)
                bad_ips += ip + "\n"
                bad_count += 1
            print(f'本次测试可用ip：{good_count}')
            print(f'本次测试不可用ip：{bad_count} / {len(new_ips)}')

            with open('ips.txt', 'w+') as f:
                f.write(good_ips)
            with open('ips_err.txt', 'w+') as f:
                f.write(bad_ips)

            print(run_index, '文件写入成功。休息' + str(time_sleep) + 's后继续',
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            timeout(time_sleep)
        except Exception as e:
            print("出错了休息60s：", e)
            errTimes += 1
            errText += f'{e}\n'
            timeout(60)
        run_index += 1

input('over')

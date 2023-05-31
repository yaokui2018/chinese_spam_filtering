# -*- coding: utf-8 -*-
# Author: 薄荷你玩
# Date: 2023/05/06
import os

import eventlet
import requests
import time
from tqdm import tqdm

from requests import RequestException
from requests_toolbelt.utils import dump

global ips, ip_index, curr_ip, err_times
ips = []
ip_index = 0
curr_ip = None
err_times = 0



def timeout(_time):
    """
    超时限制
    :param _time:睡眠时间
    :return: 是否超时
    """
    with eventlet.Timeout(_time + 10, False):  # 设置超时间
        time.sleep(_time)
        return False
    print('函数调用超时', _time)
    return True

def update_ip():
    global ips, ip_index, curr_ip
    if ip_index >= len(ips) or len(ips) == 0:
        if len(ips) > 0:
            text = "ip列表遍历完了，休息10分钟再试"
            print(text, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            timeout(60 * 10)

        with open('代理ip获取/goodIps.txt') as f:
            ips = f.readlines()
        ip_index = 0
    ip = ips[ip_index].replace("\n", "")
    ip_index += 1
    curr_ip = ip
    print("ip更新成功", ip)

def ai_chat(prompt):
    """
    从AIchatOS接口中调用ChatGPT
    :param prompt: 对话文字
    :return:
    """
    global curr_ip, err_times
    url = "http://api.binjie.fun/api/generateStream"
    # 设置代理
    proxy = {
        'http': curr_ip,
        'https': curr_ip
    }
    headers = {
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://chat2.aichatos.top",
        "referer": "https://chat2.aichatos.top/",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36"
    }
    data = {
        "prompt": f"你是一个优秀的数据标注师，你现在要做的任务是把下面的评论数据，标注成是否是垃圾评论，垃圾评论包括广告、暴力、议论政治、违反法律、脏话等不应该在论坛公开显示的内容，对于无意义的灌水评论和需要在特殊场景下有意义的评论不认为是垃圾评论。标签有 是、不是和不确定 三种情况。\n\n{prompt}",
        "userId": "#/chat/1683277785263",
        "network": False,
        "system": "",
        "withoutContext": False,
        "stream": False
    }
    try:
        response = requests.post(url, timeout=160, headers=headers, proxies=proxy, json=data)
        # response = requests.post(url, headers=headers, json=data)
        # data = dump.dump_all(response)
        # print(data.decode('utf-8'))
        if (response.status_code == 200):
            err_times = 0
            return response.content.decode('utf-8')
        else:
            return None
    except Exception as e:
        print("出错了！", e)
        if "Cannot connect to proxy" in str(e):
            err_times += 1
            return "ip_error"
        return None


def annotate_data(path, batch=100, startPos=None):
    is_spam = 0
    if 'spam' in path:
        is_spam = 1
    for file in os.listdir(path):
        fi = open(path + '/' + file, 'r', encoding='utf-8')
        lines = fi.readlines()
        prompt = ""
        commons = []
        index = 1
        for i, line in enumerate(tqdm(lines)):
            if startPos is not None and file == startPos[0] and i <= startPos[1]:
                continue
            prompt += f"{index}. " + line
            commons.append(line)
            if (i != 0 and i % batch == 0) or i == len(lines) - 1:
                # 使用 ChatGPT 重新标注
                result = ai_chat(prompt)
                while result is None or not save_data(commons, result, is_spam, file):
                    # 使用 ChatGPT 重新标注
                    result = ai_chat(prompt)
                print(file, f'进度：{i}/{len(lines)}', time.strftime("%Y-%m-%d %H:%M:%S"))
                prompt = ""
                commons.clear()
                index = 0
            index += 1
        # break


def save_data(commons, results, old_label, filename):
    """
    保存数据到文件中
    :param commons: 文本评论数据[]
    :param result: ChatGPT 标注结果
    :param old_label: 原本标注（0：normal，1：spam）
    :return:
    """
    global err_times

    if "ip_error" == results or "该ip一小时内连续请求了100次以上已被暂时限流" in results or "由于您违反了用户协议，我们已暂停您" in results or "你已经被临时封禁" in results:
        if "ip_error" == results and err_times < 5:
            return False
        print("需要更新ip", results)
        update_ip()
        err_times = 0
        return False
    else:
        labels = results.split("\n")
        for index, label in enumerate(labels):
            if ". " not in label:
                print("无效行，continue：", label)
                continue
            else:
                index = int(label.split(". ")[0]) - 1
            if ". 不是" in label or ". 正常评论" in label:
                new_label = 0
            elif ". 是" in label or ". 垃圾评论" in label:
                new_label = 1
            elif ". 不确定" in label:
                new_label = 2
                # 正常评论不确定时认为是正常的
                if old_label == 0:
                    new_label = 0
            else:
                new_label = 3
                print("************未知返回结果***********", label)
            if new_label != old_label:
                print(f"结果发生变化：【原始：{old_label == 1}，新的：{new_label == 1}({new_label})】. 原文：{commons[index].strip()}", label)
            path = 'normal/'
            if old_label == 1:
                path = 'spam/'
            file_paths = [path + 'normal_' + filename, path + 'spam_' + filename, path + 'unknown_' + filename, 'err.txt']
            with open(file_paths[new_label], 'a+', encoding='utf8') as f:
                f.write(commons[index])
    return True




if __name__ == '__main__':
    annotate_data("../normal", batch=100, startPos=['9.txt', 9500])

    # res = ai_chat("nihao", '221.193.228.7:9002')
    # print(res)
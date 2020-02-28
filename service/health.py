#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# @Time : 2020/2/28 12:19
# @Author : ActStrady@tom.com
# @FileName : health.py
# @GitHub : https://github.com/ActStrady/run
import threading
import requests
import json
import random
import time

from requests import RequestException

from util import init

# 在 centos 下解决中文不能读取错误
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

logger = init.get_log()
lock = threading.RLock()


def health(username, password, longitude, latitude):
    # 加线程锁 保证每人登录时不会同时获取
    lock.acquire()
    token = 'Bearer ' + init.get_token(username, password)
    # 释放线程锁
    lock.release()

    # 线程休眠两秒，模拟登录时间
    time.sleep(2)

    url = "http://api.tjise.edudot.cn/api/v1/Health/BodyTemperature"
    # 根据谷歌api来获取地址
    location = init.get_address(latitude, longitude)
    # 获取当前时间戳
    measureDate = lambda: int(round(time.time() * 1000))
    # 体温
    bodyTemperature = round(random.uniform(35.5, 36.7), 1)
    params = {
        'bodyTemperature': bodyTemperature,
        'isContactPatient': 0,
        'latitude': latitude,
        'longitude': longitude,
        'location': location,
        'remark': '身体健康良好，无发热咳嗽等症状，家人健康，无疑似',
        'measureTimeType': 1,
        'measureDate': measureDate()
    }
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; 16s Pro Build/PKQ1.190616.001; wv)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126'
                      ' MQQBrowser/6.2 TBS/044904 Mobile Safari/537.36; Edudot',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json;charset=UTF-8',
        'credentials': 'include',
        'Referer': 'http://clock.tjise.edudot.cn/',
        'Authorization': token,
        'Origin': 'http://clock.tjise.edudot.cn',
        'Connection': 'keep-alive',
        'Host': 'api.tjise.edudot.cn'
    }

    # 处理开始请求可能的异常
    try:
        response = requests.post(url=url, data=json.dumps(params), headers=headers)
    except RequestException:
        logger.exception("提交健康失败")
    else:
        if (response.json().get("code") == 200) & (response.json().get("data").get("result")):
            logger.info(threading.current_thread().getName() + '提交健康成功')
        else:
            logger.info(threading.current_thread().getName() + response.json().get("msg"))


if __name__ == '__main__':
    # 日志分割线
    logger.info('----------' + time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())) + '----------')
    # 使用多线程来提高效率和防止一个人出问题其他没法成功
    threading.Thread(target=health, args=(13702059309, "Tjise@0033", 113.705916, 39.703702), name='王强').start()
    # threading.Thread(target=health, args=(13194625307, "Tjise@5442", 117.479034, 39.873684), name='梁爽').start()

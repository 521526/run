# -*- coding: UTF-8 -*-
import threading
import requests
import json
import random
import time

from requests import RequestException

from util import init

# # 在 centos 下解决中文不能读取错误
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

logger = init.get_log()
lock = threading.RLock()


def run(username, password):
    # 加线程锁 保证每人登录时不会同时获取
    lock.acquire()
    token = 'Bearer ' + init.get_token(username, password)
    # 释放线程锁
    lock.release()

    # 线程休眠两秒，模拟登录时间
    time.sleep(2)

    url = "http://api.tjise.edudot.cn/api/v1/Motions/ClockIn"
    # 开始经纬度
    start_latitude = round(random.uniform(39.068189, 39.068574), 6)
    start_longitude = round(random.uniform(117.106829, 117.107081), 6)
    # 结束经纬度
    stop_latitude = round(random.uniform(39.062292, 39.06293), 6)
    stop_longitude = round(random.uniform(117.111371, 117.111913), 6)

    # 根据谷歌api来获取地址
    start_address = init.get_address(start_latitude, start_longitude)
    stop_address = init.get_address(stop_latitude, stop_longitude)
    params1 = {
        'address': start_address,
        'latitude': start_latitude,
        'longitude': start_longitude,
        'status': 0
    }
    params2 = {
        'address': stop_address,
        'latitude': stop_latitude,
        'longitude': stop_longitude,
        'status': 1
    }
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9.0; ONEPLUS A6000 Build/PKQ1.180716.001; wv) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 '
                      'Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044306 Mobile '
                      'Safari/537.36; Edudot',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json;charset=UTF-8',
        'credentials': 'include',
        'Referer': 'http://clock.tjise.edudot.cn/',
        'Authorization': token,
        'Origin': 'http://clock.tjise.edudot.cn',
        'Connection': 'keep-alive',
        'Host': 'api.tjise.edudot.cn'
    }

    # 处理开始跑步请求可能的异常
    try:
        start_response = requests.post(url=url, data=json.dumps(params1), headers=headers)
    except RequestException:
        logger.exception("start run error")
    else:
        if (start_response.json().get("code") == 200) & (start_response.json().get("data").get("status")):
            logger.info(threading.current_thread().getName() + '晨跑开始!')
        else:
            logger.info(threading.current_thread().getName() + start_response.json().get("data").get("msg"))

    # 线程休眠十分钟，模拟用户跑步
    time.sleep(600)

    # 处理结束跑步请求可能的异常
    try:
        stop_response = requests.post(url=url, data=json.dumps(params2), headers=headers)
    except RequestException:
        logger.exception('stop run error')
    else:
        if (stop_response.json().get("code") == 200) & (stop_response.json().get("data").get("status")):
            logger.info(threading.current_thread().getName() + '晨跑结束!')
        else:
            logger.info(threading.current_thread().getName() + stop_response.json().get("data").get("msg"))


if __name__ == '__main__':
    # 日志分割线
    logger.info('----------' + time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())) + '----------')
    # 使用多线程来提高效率和防止一个人出问题其他没法成功
    threading.Thread(target=run, args=(13702059309, "Tjise@0033"), name='王强').start()
    threading.Thread(target=run, args=(13102263173, "168668"), name='王娇').start()
    threading.Thread(target=run, args=(17695538053, "Tjise@121X"), name='韩思远').start()
    threading.Thread(target=run, args=(18222043061, "Tjise@0233"), name='杨恒').start()
    threading.Thread(target=run, args=(13072261182, "960307"), name='王雯').start()
    threading.Thread(target=run, args=(13752667961, "Tjise@3340"), name='张研').start()
    threading.Thread(target=run, args=(13207625187, "Tjise@001X"), name='秦鸣林').start()
    threading.Thread(target=run, args=(17695490892, "Tjise@0424"), name='刘子靖').start()
    threading.Thread(target=run, args=(15160028860, "a123456"), name='王勃阳').start()
    threading.Thread(target=run, args=(18980712647, "Tjise@6712"), name='邓桥阳').start()
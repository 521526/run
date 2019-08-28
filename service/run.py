# -*- coding: UTF-8 -*-
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


def run(username, password, num):
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
    # run起始结束位置
    start_addresses = ('天津市西青区工西路18号靠近天津工业大学公寓', '天津市西青区工西路18号靠近天津工业大学新校区',
                       '天津市西青区泮缘道18号靠近天津工业大学新校区', '天津市西青区S6津沧高速18号靠近天津工业大学公寓',
                       '天津市西青区工西路18号靠近天津大学软件学院学术交流中心', '天津市西青区西环路18号靠近天津市大学软件学院')
    stop_addresses = ('天津市西青区镜缘道20号靠近天津工业大学图书馆', '天津市西青区西环路18号靠近天津工业大学外国语学院',
                      '天津市西青区西环西路18号靠近天津工业大学新校区经济学院', '天津市西青区西环路18号靠近天津工业大学新校区经济学院')
    start_address = random.choice(start_addresses)
    stop_address = random.choice(stop_addresses)
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
    headers = init.get_location(start_latitude, start_longitude, token, num)
    # 处理开始跑步请求可能的异常
    try:
        requests.post(url=url, data=json.dumps(params1), headers=headers)
    except RequestException:
        logger.exception("start run error")
    else:
        pass
        url = 'http://api.tjise.edudot.cn/api/v1/Motions/GetSignInState?'
        time.sleep(2)
        response = requests.get(url=url, headers=headers)
        logger.info(threading.current_thread().getName() + ':开始跑步' + response.json().get("data").get("failReason"))

    # 线程休眠十分钟，模拟用户跑步
    time.sleep(600)

    # 结束跑步
    url = "http://api.tjise.edudot.cn/api/v1/Motions/ClockIn"
    headers = init.get_location(stop_latitude, stop_longitude, token, num)
    # 处理结束跑步请求可能的异常
    try:
        requests.post(url=url, data=json.dumps(params2), headers=headers)
    except RequestException:
        logger.exception('stop run error')
    else:
        url = 'http://api.tjise.edudot.cn/api/v1/Motions/GetSignInState?'
        time.sleep(2)
        response = requests.get(url=url, headers=headers)
        logger.info(threading.current_thread().getName() + ':结束跑步' + response.json().get("data").get("failReason"))


if __name__ == '__main__':
    # 日志分割线
    logger.info('----------' + time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())) + '----------')
    # 使用多线程来提高效率和防止一个人出问题其他没法成功
    threading.Thread(target=run, args=(13702059309, "Tjise@0033", 0), name='王强').start()
    # threading.Thread(target=run, args=(13102263173, "168668"), name='王娇').start()
    threading.Thread(target=run, args=(17695538053, "Tjise@121X", 1), name='韩思远').start()
    threading.Thread(target=run, args=(18222043061, "Tjise@0233", 2), name='杨恒').start()
    threading.Thread(target=run, args=(13072261182, "960307", 3), name='王雯').start()
    threading.Thread(target=run, args=(13752667961, "Tjise@3340", 4), name='张研').start()
    threading.Thread(target=run, args=(13207625187, "Tjise@001X", 3), name='秦鸣林').start()
    threading.Thread(target=run, args=(17695490892, "Tjise@0424", 5), name='刘子靖').start()
    threading.Thread(target=run, args=(15160028860, "a123456", 6), name='王勃阳').start()
    # threading.Thread(target=run, args=(18980712647, "Tjise@6712"), name='邓桥阳').start()

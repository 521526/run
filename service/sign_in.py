# -*- coding: UTF-8 -*-
import threading

import requests
import json
import time
import random
from util import init

# 在 centos 下解决中文不能读取错误
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

logger = init.get_log()
lock = threading.RLock()


def sign_in(username, password):
    # 加线程锁 保证每人登录时不会同时获取
    lock.acquire()
    token = 'Bearer ' + init.get_token(username, password)
    # 释放线程锁
    lock.release()

    # 线程休眠两秒，模拟登录时间
    time.sleep(2)

    url = 'http://api.tjise.edudot.cn/api/v1/LateSignIn/SignIn'
    # 纬度
    latitude = round(random.uniform(39.069051, 39.06282), 6)
    # 经度
    longitude = round(random.uniform(117.106303, 117.109533), 6)

    # 定义地址列表
    addresses = ('天津市西青区工西路18号靠近天津工业大学公寓', '天津市西青区工西路18号靠近天津工业大学新校区',
                 '天津市西青区泮缘道18号靠近天津工业大学新校区', '天津市西青区S6津沧高速18号靠近天津工业大学公寓',
                 '天津市西青区工西路18号靠近天津大学软件学院学术交流中心', '天津市西青区西环路18号靠近天津市大学软件学院')
    address = random.choice(addresses)
    params = {
        'signInLocation': address,
        'remark': '',
        'latitude': latitude,
        'longitude': longitude,
    }
    # 0-8随机数来取头数据
    num = random.randint(0, 7)
    # 模拟获取地址
    headers = init.get_location(latitude, longitude, token, num)
    try:
        requests.post(url=url, data=json.dumps(params), headers=headers)
    except Exception as e:
        logger.exception("签到请求异常", e)
    else:
        url = 'http://api.tjise.edudot.cn/api/v1/LateSignIn/GetLateSignInStatus?'
        time.sleep(2)
        response = requests.get(url=url, headers=headers)
        logger.info(threading.current_thread().getName() + ':' + response.json().get("data").get("failReason"))


if __name__ == '__main__':
    # 日志分割线
    logger.info('----------' + time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())) + '----------')
    # 使用多线程来提高效率和防止一个人出问题其他没法成功
    threading.Thread(target=sign_in, args=(13702059309, "", 0), name='王强').start()

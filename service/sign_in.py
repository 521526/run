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

    # 使用谷歌api获取地址传入到请求参数
    address = init.get_address(latitude, longitude)
    params = {
        'signInLocation': address,
        'remark': '',
        'latitude': latitude,
        'longitude': longitude,
    }
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '143',
        'Authorization': token,
        'Origin': 'http://clock.tjise.edudot.cn',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9.0; ONEPLUS A6000 Build/PKQ1.180716.001; wv) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 '
                      'Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044306 Mobile '
                      'Safari/537.36; Edudot',
        'credentials': 'include',
        'Content-Type': 'application/json;x-www-form-urlencode;charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': '*/*',
        'Referer': 'http://clock.tjise.edudot.cn/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8'
    }

    try:
        response = requests.post(url=url, data=json.dumps(params), headers=headers)
    except Exception as e:
        logger.exception("签到请求异常", e)
    else:
        if (response.json().get("code") == 200) & (response.json().get("data").get("result")):
            logger.info(threading.current_thread().getName() + '签到成功！')
            logger.info(response.json())
        else:
            logger.info(threading.current_thread().getName() + response.json().get("data").get("reason"))


if __name__ == '__main__':
    # 日志分割线
    logger.info('----------' + time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())) + '----------')
    # 使用多线程来提高效率和防止一个人出问题其他没法成功
    threading.Thread(target=sign_in, args=(13702059309, "Tjise@0033"), name='王强').start()
    # threading.Thread(target=sign_in, args=(13102263173, "168668"), name='王娇').start()
    # threading.Thread(target=sign_in, args=(17695538053, "Tjise@121X"), name='韩思远').start()
    # threading.Thread(target=sign_in, args=(18222043061, "Tjise@0233"), name='杨恒').start()
    # threading.Thread(target=sign_in, args=(13072261182, "960307"), name='王雯').start()
    # threading.Thread(target=sign_in, args=(13752667961, "Tjise@3340"), name='张研').start()
    # threading.Thread(target=sign_in, args=(13207625187, "Tjise@001X"), name='秦鸣林').start()
    # threading.Thread(target=sign_in, args=(17695490892, "Tjise@0424"), name='刘子靖').start()
    # threading.Thread(target=sign_in, args=(15160028860, "a123456"), name='王勃阳').start()
    # threading.Thread(target=sign_in, args=(18980712647, "Tjise@6712"), name='邓桥阳').start()

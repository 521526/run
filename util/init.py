# -*- coding: UTF-8 -*-
import logging
import requests

from requests import RequestException


# 获取日志
def get_log():
    logger = logging.getLogger(__name__)

    # 格式化
    for_mat = logging.Formatter('%(asctime)s - %(module)s - %(lineno)d - %(levelname)s - %(message)s')
    # 文件log
    file_handler = logging.FileHandler('log.txt', encoding='utf-8')
    # 控制台log
    console_handler = logging.StreamHandler()
    # 设置格式
    file_handler.setFormatter(for_mat)
    console_handler.setFormatter(for_mat)

    # 日志级别
    logger.setLevel(logging.INFO)

    # 确保日志打印一次
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger


# 登录获取token
def get_token(username, password):
    url = "http://api.edudot.cn/usercenter/connect/token"

    params = {
        'password': password,
        'grant_type': 'password',
        'login_type': '',
        'client_id': 'DDE1F5ACAF194674B13167269861FB7D',
        'username': username
    }

    headers = {
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.4.2',
        'Content-Length': '117',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': '',
        'Connection': 'Keep-Alive',
        'Host': 'api.edudot.cn'
    }

    # 捕获request的异常
    try:
        response = requests.post(url=url, data=params, headers=headers)
    except RequestException:
        get_log().exception('get_token error')
    else:
        return response.json().get('access_token')


def get_location(latitude, longitude, token):
    """
    模拟获取地址
    :param latitude: 维度
    :param longitude: 经度
    :param token: 登录的token
    :return:
    """
    url = 'http://api.tjise.edudot.cn/api/v1/LateSignIn/GetLocation' \
          '?latitude={}&longitude={}'.format(latitude, longitude)
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Authorization': token,
        'Origin': 'http://clock.tjise.edudot.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; M6 Note Build/N2G47H; wv) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 '
                      'MQQBrowser/6.2 TBS/044704 Mobile Safari/537.36; Edudot',
        'credentials': 'include',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': '*/*',
        'Referer': 'http://clock.tjise.edudot.cn/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.9'
    }
    requests.get(url=url, headers=headers)
    return headers

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


# 获取token
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
        'User-Agent': 'okhttp/3.3.1',
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


def get_address(latitude, longitude):
    url = 'https://restapi.amap.com/v3/geocode/regeo?key=48fec8bff8b03cd5dbec69715adec53e&location='\
          + str(longitude) + ',' + str(latitude) + '&radius=1000&extensions=all&batch=false&roadlevel=1'
    response = requests.get(url=url)
    address = response.json().get("regeocode").get("formatted_address")
    return address

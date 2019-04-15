import requests
import json
import time
import random


def gettoken():
    url = "http://api.edudot.cn/usercenter/connect/token"

    params = {
        'password': 'Tjise@1016',
        'grant_type': 'password',
        'login_type': '',
        'client_id': 'DDE1F5ACAF194674B13167269861FB7D',
        'username': 17695959564
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

    response = requests.post(url=url, data=params, headers=headers)
    return response.json().get('access_token')


def running():
    token = 'Bearer ' + gettoken()

    url = "http://api.tjise.edudot.cn/api/v1/Motions/ClockIn"

    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9.0; ONEPLUS A6000 Build/PKQ1.180716.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044306 Mobile Safari/537.36; Edudot',
        'X-Requested-With': 'XMLHttpRequest',
        #'Content-Length': 135,
        'Content-Type': 'application/json;charset=UTF-8',
        'credentials': 'include',
        'Referer': 'http://clock.tjise.edudot.cn/',
        'Authorization': token,
        'Origin': 'http://clock.tjise.edudot.cn',
        'Connection': 'keep-alive',
        'Host': 'api.tjise.edudot.cn'
    }

    stoplatitude = round(random.uniform(39.062292, 39.06293), 6)         # 纬度
    stoplongitude = round(random.uniform(117.111371, 117.111913), 6)      # 经度

    stopaddressurl = 'https://restapi.amap.com/v3/geocode/regeo?key=48fec8bff8b03cd5dbec69715adec53e&location='+ str(stoplongitude) + ',' + str(stoplatitude) + '&radius=1000&extensions=all&batch=false&roadlevel=1'
    response = requests.get(url=stopaddressurl)
    stopaddress = response.json().get("regeocode").get("formatted_address")

    params2 = {
        'address': '天津工业大学新校区',
        'latitude': stoplatitude,
        'longitude': stoplongitude,
        'status': 1
    }

    response = requests.post(url=url, data=json.dumps(params2), headers=headers)
    print(response.json())

    if response.json().get("code") == 200:
        #print('结束跑步的地址(;￢д￢) :' + str(params2))
        print('晨跑结束(•‾̑⌣‾̑•)✧˖°')
    else:
        print('结束失败(︶︹︺)')


if __name__ == '__main__':
    running()

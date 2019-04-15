'''
# 天软签到

    V 1.0 
    ---- 调用谷歌API利用经纬度获取地址名称

    V 1.1
    ---- 将地址改为固定'天津工业大学新校区'


注：
    ---- 在gettoken()函数的params中填写自己的password和username，password用单引号引起来，username不用引

                                                    ————————  by 蛋蛋超人
'''


import requests
import json
import time
import random


def gettoken():
    url = "http://api.edudot.cn/usercenter/connect/token"

    params = {
        'password': '0',
        'grant_type': 'password',
        'login_type': '',
        'client_id': 'DDE1F5ACAF194674B13167269861FB7D',
        'username': 0
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
    # print(response.json())
    return response.json().get('access_token')


def qiandao():

    token = 'Bearer ' + gettoken()
    time.sleep(3)

    latitude = round(random.uniform(39.069051, 39.06282), 6)         # 纬度
    longitude = round(random.uniform(117.106303, 117.109533), 6)      # 经度

    # 利用谷歌API根据经纬度获取地址
    addressurl = 'https://restapi.amap.com/v3/geocode/regeo?key=48fec8bff8b03cd5dbec69715adec53e&location='+ str(longitude) + ',' + str(latitude) + '&radius=1000&extensions=all&batch=false&roadlevel=1'
    response = requests.get(url=addressurl)
    address = response.json().get("regeocode").get("formatted_address")

    params = {
        'signInLocation': '天津工业大学新校区',
        'remark': '',
        'latitude': latitude,
        'longitude': longitude,
    }
    #print('签到地址( ﹁ ﹁ ) ：' + str(params))

    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '143',
        'Authorization': token,
        'Origin': 'http://clock.tjise.edudot.cn',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9.0; ONEPLUS A6000 Build/PKQ1.180716.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044306 Mobile Safari/537.36; Edudot',
        'credentials': 'include',
        'Content-Type': 'application/json;x-www-form-urlencode;charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': '*/*',
        'Referer': 'http://clock.tjise.edudot.cn/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8'
    }
    url = 'http://api.tjise.edudot.cn/api/v1/LateSignIn/SignIn'

    response = requests.post(url=url, data=json.dumps(params), headers=headers)

    print(response.json())
    if response.json().get("code") == 200:
        print("签到成功(•‾̑⌣‾̑•)✧˖°")
    else:
        print("签到失败")


if __name__ == '__main__':
    qiandao()

import pymysql
import requests
import re
import sys
import os
import json

# 接口的请求头
headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; 21051182C Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.166 Safari/537.36 App/boohee/7.5.6',
    'token': 'Wwq3kjpeyPp7DmDv2zsVVFp5Gqw3N19u',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Origin': 'https://foodie.boohee.com',
    'X-Requested-With': 'com.boohee.one',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://foodie.boohee.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}


# 请求超时重连
def getHtml(url):
    i = 0
    while i < 3:
        try:
            return requests.get(url, timeout=(5, 5), headers=headers).text
        except requests.exceptions.RequestException:
            print('--')
            i += 1


# print(getHtml("https://food.boohee.com/fb/v2/foods/qingchaojiuhuang/detail"))
# 连接数据库
connect = pymysql.connect(host="localhost", port=3306, user="root", password="123456++q", database="dishes",
                          client_flag=10, charset="utf8mb4")

cursor = connect.cursor()


def getJsonFile(p):
    if os.path.exists(p):
        if sys.version_info.major > 2:
            f = open(p, 'r', encoding='utf-8')
        else:
            f = open(p, 'r')
    return json.load(f)


foods = getJsonFile(r'd:\Download\foods.json')
allSize = len(foods)
i = 0
for food in foods:
    basic_info = food['basic_info']
    food_name = basic_info['food_name']
    i = i + 1
    print(str(i) + "-" + str(allSize) + food_name)
    food_type = basic_info['food_group_name']
    img = basic_info['img_big_href']
    materials = str(food['material_info']).replace("'", '"')
    code_name = str(food['href']).replace('http://www.boohee.com/shiwu/', '').replace("'", '"')
    production_method = str(food['production_method']).replace("'", '"')
    info = json.loads(getHtml('https://food.boohee.com/fb/v2/foods/' + code_name + '/detail'))
    suitable = {}
    taboo = {}
    for tag in info['scenes']:
        if tag['suitable']:
            suitable = {'name': tag['name'], 'tags': tag['tags']}
        elif not tag['suitable']:
            taboo = {'name': tag['name'], 'tags': tag['tags']}
    try:
        # 插入数据库
        sql = "INSERT INTO food (fid,food_name,food_group,suitable,taboo,materials,production_method,img) \
                    VALUE('%s','%s','%s','%s','%s','%s','%s','%s')" \
              % (
              code_name, food_name, food_type, str(suitable).replace("'", '"'), str(taboo).replace("'", '"'), materials,
              production_method, img)
        cursor.execute(sql)
        connect.commit()
    except:
        print('错误')

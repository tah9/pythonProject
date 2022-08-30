import requests
import json
import pymysql

headers = {
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 11; 21051182C Build/RKQ1.200826.002) (#Build; Xiaomi; 21051182C; RKQ1.200826.002 test-keys; 11) +CoolMarket/7.5',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Sdk-Int': '30',
    'X-Sdk-Locale': 'zh-CN',
    'X-App-Id': 'com.coolapk.market',
    'X-App-Token': 'c1ca1131dab85ebdca3d6579fbf3ffd651c07174-d3cf-3f21-aceb-a4aea81f1c700x6156c012',
    'X-App-Version': '7.5',
    'X-App-Code': '1703162',
    'X-Api-Version': '7',
    'Host': 'api.coolapk.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
}
connect = pymysql.connect(host="localhost", port=3306, user="root", password="123456++q", database="graduate_run",
                          client_flag=10, charset="utf8mb4")

cursor = connect.cursor()

def gethtml(url):
  i = 0
  while i < 3:
    try:
      html = requests.get(url, timeout=(5,5),headers=headers)
      return html
    except requests.exceptions.RequestException:
      i += 1

def inserFollow(uid):
    rows=json.loads(gethtml('https://api.coolapk.com/v6/user/followList?uid='+str(uid)+'&page=1').text)['data']
    for user in rows:
        print(user)
        print(user['uid'],user['fuid'])
        que = 'SELECT 1 FROM sys_user WHERE uid=' + str(user['fuid']) + ' LIMIT 1'
        cursor.execute(que)
        sqlUser = cursor.fetchone()
        print(sqlUser)
        fuser=user['fUserInfo']
        #插入被关注者
        if sqlUser is None:
            sql = "insert into sys_user(uid,username,userAvatar,cover,logintime) \
                                                 value('%s','%s','%s','%s','%s')" \
                  % (fuser.get('uid'), fuser.get('username'),
                     fuser.get('userAvatar'), fuser.get('cover'), fuser.get('logintime'))
            cursor.execute(sql)
            print('插入用户>>' + str(user['uid']))
        # 插入关注关系
        sql2="insert into user_fans(uid,follow_id) value('%s','%s')" % (user['uid'],user['fuid'])
        cursor.execute(sql2)
        connect.commit()
# def updateUser(id):
#     user=json.loads(gethtml('https://api.coolapk.com/v6/user/space?uid='+str(id)).text)['data']
#     que = 'SELECT 1 FROM sys_user WHERE uid=' + str(id) + ' LIMIT 1'
#     cursor.execute(que)
#     sqlUser = cursor.fetchone()
#     if sqlUser is None:
#         sql = "insert into sys_user(uid,username, password,phone_number,userAvatar,cover,logintime,gender,bio,follow,fans,be_like_num) \
#                                       value('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
#               % (user.get('uid'), user.get('username'),
#                  '$2a$10$WkZgmfNnYb8ufXoRDpm7c.tx9Ejnfg1ccIv5L6uXLg695J/lq2.YC', user.get('uid'),
#                  user.get('userAvatar'), user.get('cover'), user.get('logintime'),
#                  user['gender'],user['bio'],user['follow'],user['fans'],user['be_like_num'],)
#         cursor.execute(sql)
#         print('插入用户>>' + str(user['uid']))
#     else:
#         sql2="UPDATE sys_user SET gender=%s ,bio=%s ,follow=%s ,fans=%s ,be_like_num=%s WHERE uid=%s"
#         update_data = [str(user['gender']),str(user['bio']),str(user['follow']),str(user['fans']),str(user['be_like_num']),str(id) ]
#         cursor.execute(sql2, update_data)
#         print('修改用户>>' + str(user['uid']))
#     connect.commit()
def getAllArticle():
    sql = "SELECT uid FROM article"
    cursor.execute(sql)
    result=cursor.fetchall()
    for item in result:
        inserFollow(item[0])









getAllArticle()













connect.close()

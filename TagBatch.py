import requests
import json
import pymysql
headers = {
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 11; 21051182C Build/RKQ1.200826.002) (#Build; Xiaomi; 21051182C; RKQ1.200826.002 test-keys; 11) +CoolMarket/7.5',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Sdk-Int': '30',
    'X-Sdk-Locale': 'zh-CN',
    'X-App-Id': 'com.coolapk.market',
    'X-App-Token': '469b208b93e72d2c26d8a358418a6e4c51c07174-d3cf-3f21-aceb-a4aea81f1c700x6154693b',
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


def insert(item):
    userRows=item['recent_follow_list']
    follow_list = ''
    for userInfo in userRows:
        user=userInfo['userInfo']
        follow_list=follow_list+','+str(user['uid'])
        que = 'SELECT 1 FROM sys_user WHERE uid=' + str(user['uid']) + ' LIMIT 1'
        cursor.execute(que)
        sqlUser = cursor.fetchone()
        if sqlUser is None:
            insertUser(user)
    inserTag(item,follow_list)
    connect.commit()

def inserTag(data,follow_list):
    follow_list=follow_list.strip(',')
    print(str(follow_list))
    print(str(data))
    sql="INSERT INTO article_tags (id,title,logo,cover,description,follownum,hot_num,dateline,lastupdate,feednum,intro,follow_list,keywords) \
            VALUE('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
            % (data['id'],data['title'],data['logo'],data['cover'],
               data['description'],data['follownum'],data['hot_num'],
               data['dateline'],data['lastupdate'],data['feednum'],data['intro'],str(follow_list),data['keywords'])
    cursor.execute(sql)
    print('插入专题>>' + str(data['id']))

def insertUser(user):
    sql = "insert into sys_user(uid,username, password,phone_number,userAvatar,cover,logintime) \
                                       value('%s','%s','%s','%s','%s','%s','%s')" \
                  % (user.get('uid'), user.get('username'),
                     '$2a$10$WkZgmfNnYb8ufXoRDpm7c.tx9Ejnfg1ccIv5L6uXLg695J/lq2.YC', user.get('uid'),
                     user.get('userAvatar'), user.get('cover'), user.get('logintime'))
    cursor.execute(sql)
    print('插入用户>>' + str(user['uid']))

def pageLoad(rows):
    for data in rows:
        myjson=gethtml('https://api.coolapk.com/v6/topic/tagDetail?tag='+str(data['title']))
        insert(json.loads(myjson.text)['data'])

#爬取专题
def tagsAllArticle():
    i = 13
    while True:
        #运动健身
        url = 'https://api.coolapk.com/v6/topic/tagList?page=' + str(i)
        print('开始第'+str(i)+'页')
        rows = json.loads(gethtml(url).text)
        if 'data' in rows:
            pageLoad(rows['data'])
            print('结束第'+str(i)+'页')
            i = i + 1
        else:
            print('专题抓取完成')
            break
tagsAllArticle()
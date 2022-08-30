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

def inserArticle(id):
    # 查看动态详情
    aurl = 'https://api.coolapk.com/v6/feed/detail?id=' + str(id)
    article = gethtml(aurl).text
    data = json.loads(article)
    item = data['data']

    # print(item)
    user = item['userInfo']
    # print(user)
    que = 'SELECT 1 FROM sys_user WHERE uid=' + str(user['uid']) + ' LIMIT 1'
    cursor.execute(que)
    sqlUser = cursor.fetchone()
    if sqlUser is None:
        sql = "insert into sys_user(uid,username, password,phone_number,userAvatar,cover,logintime) \
                                   value('%s','%s','%s','%s','%s','%s','%s')" \
              % (user.get('uid'), user.get('username'),
                 '$2a$10$WkZgmfNnYb8ufXoRDpm7c.tx9Ejnfg1ccIv5L6uXLg695J/lq2.YC', user.get('uid'),
                 user.get('userAvatar'), user.get('cover'), user.get('logintime'))
        cursor.execute(sql)
        print('插入用户>>' + str(user['uid']))
    pics = json.dumps(item['picArr']).replace('"', '').replace("[", '').replace(']', '').replace(' ', '')
    # print(pics)
    queArticle = 'SELECT 1 FROM article WHERE id=' + str(item['id']) + ' LIMIT 1'
    cursor.execute(queArticle)
    verArticle = cursor.fetchone()
    if verArticle is None:
        sql2 = "INSERT INTO article(id,message_title,message,uid,likenum,commentnum" \
               ",favnum,dateline,tags,device_title,rank_score,pic,share_num,message_cover" \
               ",recent_reply_ids,recent_hot_reply_ids,feedType,replynum) \
                                   VALUE('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
               % (item['id'], item['message_title'], item['message'],
                  item['uid'], item['likenum'], item['commentnum'],
                  item['favnum'], item['dateline'], item['tags'],
                  item['device_title'], item['rank_score'],
                  pics, item['share_num'], item['message_cover'],
                  item['recent_reply_ids'],item['recent_hot_reply_ids'],item['feedType'],item['replynum'])
        cursor.execute(sql2)
        print('插入动态>>' + str(item['id']))
    else:
        sql3="UPDATE article SET replynum=%s WHERE id=%s"
        update_data=[str(item['replynum']),str(item['id'])]
        cursor.execute(sql3, update_data)
        print('修改动态>>'+ str(item['id']))
    connect.commit()


#遍历一页
def pageLoad(rows):

    #查询每个动态详情
    for item in rows:
       print(item)
       inserArticle(item['id'])
    # data=cursor.fetchall()
    # print(data)


def gethtml(url):
  i = 0
  while i < 3:
    try:
      html = requests.get(url, timeout=(5,5),headers=headers)
      return html
    except requests.exceptions.RequestException:
      i += 1

#爬取专题下所有动态
def tagsAllArticle():
    i = 0
    while True:
        #运动健身
        # url = 'https://api.coolapk.com/v6/topic/tagFeedList?tag=%E8%BF%90%E5%8A%A8%E5%81%A5%E8%BA%AB&page=' + str(i)
        #酷安夜话
        url='https://api.coolapk.com/v6/comment/search?q=%E9%85%B7%E5%AE%89%E5%A4%9C%E8%AF%9D&page='+str(i)
        #骑行
        # url='https://api.coolapk.com/v6/topic/tagFeedList?tag=%E9%AA%91%E8%A1%8C&page='+str(i)
        #跑步
        # url='https://api.coolapk.com/v6/topic/tagFeedList?tag=%E8%B7%91%E6%AD%A5&page='+str(i)
        print('开始第'+str(i)+'页')
        rows = json.loads(gethtml(url).text)
        if 'data' in rows:
            pageLoad(rows['data'])
            print('结束第'+str(i)+'页')
            i = i + 1
        else:
            print('专题抓取完成')
            break

# inserArticle(20268181)
tagsAllArticle()
connect.close()

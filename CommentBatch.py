import requests
import json
import pymysql

headers = {
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 11; 21051182C Build/RKQ1.200826.002) (#Build; Xiaomi; 21051182C; RKQ1.200826.002 test-keys; 11) +CoolMarket/7.5',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Sdk-Int': '30',
    'X-Sdk-Locale': 'zh-CN',
    'X-App-Id': 'com.coolapk.market',
    'X-App-Token': 'c1b5fdb522222c1ffd07810d60e38cce51c07174-d3cf-3f21-aceb-a4aea81f1c700x615316cb',
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


def insert(rows):
    for item in rows:
        # print(str(item))
        #判断是否存在此用户
        qUser = 'SELECT 1 FROM sys_user WHERE uid=' + str(item['uid']) + ' LIMIT 1'
        cursor.execute(qUser)
        resultUser=cursor.fetchone()
        print(item)
        #不存在此用户就插入
        if resultUser is None:
            user = item['userInfo']
            sql = "insert into sys_user(uid,username, password,phone_number,userAvatar,cover,logintime) \
                                           value('%s','%s','%s','%s','%s','%s','%s')" \
                  % (user.get('uid'), user.get('username'),
                     '$2a$10$WkZgmfNnYb8ufXoRDpm7c.tx9Ejnfg1ccIv5L6uXLg695J/lq2.YC', user.get('uid'),
                     user.get('userAvatar'), user.get('cover'), user.get('logintime'))
            cursor.execute(sql)
            print('插入用户>>' + str(user['uid']))
        #判断是否存在此评论
        qComment='SELECT 1 FROM article_comment WHERE id=' + str(item['id']) + ' LIMIT 1'
        cursor.execute(qComment)
        resultComment=cursor.fetchone()
        #不存在此评论就插入
        if resultComment is None:
            sql2 = "insert into article_comment(id,fid,uid,rid,rrid,replynum,message,likenum,dateline,pic,rusername,feedUid,isFeedAuthor,rank_score,recent_reply_ids) \
             value('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
            % (item['id'],item['fid'],item['uid']
               ,item['rid'],item['rrid'],item['replynum']
               ,item['message'],item['likenum'],item['dateline']
               ,item['pic'],item['rusername'],item['feedUid'],item['isFeedAuthor']
               ,item['rank_score'],item['recent_reply_ids'])
            cursor.execute(sql2)
            print('插入评论>>' + str(item['id']))
        connect.commit()
def commentFatch(articleId):
    #评论页数未知
    print('开始插入'+str(articleId)+'动态下评论')
    j=1
    while True:
        curl='https://api.coolapk.com/v6/feed/replyList?id='+str(articleId)+'&page='+str(j)
        commentRows=json.loads(gethtml(curl).text)['data']
        insert(commentRows)
        j=j+1
        if len(commentRows) == 0:
            break
    print('结束插入')

def pagesFatch(rows):
    for article in rows:
        print('动态id>>'+str(article['id']))
        commentFatch(article['id'])
        print('完成插入')

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
        # 运动健身
        # url = 'https://api.coolapk.com/v6/topic/tagFeedList?tag=%E8%BF%90%E5%8A%A8%E5%81%A5%E8%BA%AB&page=' + str(i)
        # 酷安夜话
        url='https://api.coolapk.com/v6/comment/search?q=%E9%85%B7%E5%AE%89%E5%A4%9C%E8%AF%9D&page='+str(i)
        # 骑行
        # url='https://api.coolapk.com/v6/topic/tagFeedList?tag=%E9%AA%91%E8%A1%8C&page='+str(i)
        # 跑步（开始）
        # url = 'https://api.coolapk.com/v6/topic/tagFeedList?tag=%E8%B7%91%E6%AD%A5&page=' + str(i)
        print('开始第'+str(i)+'页')
        rows = json.loads(gethtml(url).text)
        if 'data' in rows:
            pagesFatch(rows['data'])
            print('结束第'+str(i)+'页')
            i = i + 1
        else:
            print('专题抓取完成')
            break

# commentFatch(20268181)

tagsAllArticle()
connect.close()


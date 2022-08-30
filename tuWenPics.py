import requests
import json
'''
图片下载
@:param url_info ('http://img.xixik.net/custom/section/country-flag/xixik-cdaca66ba3839767.png','北马里亚纳群岛)
'''
def download_img(url_info,i):
    if url_info[1]:
        print("-----------正在下载图片 %s"%(url_info))
        # 这是一个图片的url
        try:
            url = url_info
            response = requests.get(url)
            # 获取的文本实际上是图片的二进制文本
            img = response.content
            # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
            #保存路径
            path='D:\\graduate\\articlepics\\%s.jpg' % (i)
            with open(path, 'wb') as f:
                f.write(img)
        except Exception as ex:
            print("--------出错继续----")
            pass
res=requests.get('http://localhost:9001/article/getFeedArticle?pagerNum=1').text
myjson=json.loads(res)
a=0
for item in myjson:
    download_img(item['message_cover'],a)
    a=a+1
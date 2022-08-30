import pymysql
import requests
import re


def req_3(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/51.0.2704.103 Safari/537.36 '
    }
    # 自动重连3次，否则跳过
    retry_i = 0
    while retry_i < 3:
        try:
            html = requests.get(url, timeout=(5, 5), headers=headers)
            return html.text
        except requests.exceptions.RequestException:
            retry_i += 1


def search_thing(keyword):
    url = 'https://search.jd.com/Search?keyword=' + str(keyword)
    print('搜索路径：' + url)
    return req_3(url)


def get_search_sku_ids(html):
    result = re.findall('data-sku=\"(.*?)\" data-spu', html)
    return result


def get_search_spu_ids(html):
    result = re.findall('data-spu=\"(.*?)\"', html)
    return result


def get_thing_html(thing_id):
    url = 'https://item.jd.com/' + str(thing_id) + '.html'
    return req_3(url)


def get_price(html):
    temp = re.findall('<div class="p-price">(.*?)</div>', html, re.S)
    return re.findall('">(.*?)</i>', str(temp), re.S)


def get_pics(html):
    lis = re.findall('class="lh">(.*?)</ul>', html, re.S)  # res.S匹配多行

    urls = re.findall('src=\'(.*?)\'', str(lis))
    results = []
    for item in urls:
        results.append('https:' + str(item).replace('n5/s54x54_jfs', 'n1/s450x450_jfs'))
    return str(results).replace('\'', '"')


def get_name(html):
    temp = re.findall('<div class="sku-name">(.*?)</div>', html, re.S)[0]
    if '>' in temp:
        return str(temp).split('>')[1].replace(' ', '')
    else:
        return temp.replace(' ', '')


def get_info_pics(thing_id, thing_spu):
    url = 'https://cd.jd.com/description/channel?skuId=' + str(thing_id) + '&mainSkuId=' + str(
        thing_spu) + '&charset=utf-8&cdn=2&callback=showdesc'
    print(url)
    html = req_3(url)
    lists = []
    try:
        results = re.findall('//img(.*?)[\\\\|)]', html)
        for item in results:
            lists.append('https://img' + item)
    except:
        print(html)
    return str(lists).replace('\'', '"')


def insert_sql(name, price, pics, infos):
    try:
        # 插入数据库
        sql = "INSERT INTO thing (name,price,pics,more) \
                    VALUE('%s','%s','%s','%s')" \
              % (name, price, pics, infos)
        print(sql)
        cursor.execute(sql)
        connect.commit()
        print('插入完成')
    except:
        print(name, price, pics, infos)
        pass


# 连接数据库
connect = pymysql.connect(host="localhost", port=3306, user="root", password="123456++q", database="babyshop",
                          client_flag=10, charset="utf8mb4")
cursor = connect.cursor()

names = '奶瓶 纸尿片 尿不湿 婴儿车 摇摇椅 吸奶器 婴儿奶粉 拉拉裤 婴儿护肤 婴儿洗澡 婴儿洗 婴儿肚兜' \
        ' 婴儿连体衣 婴童湿巾 婴童洗漱 婴儿玩具 调奶器 婴儿百天'.split(' ')

for n in names:
    search_html = search_thing(str(n))
    # print(search_html)
    list_ids = get_search_sku_ids(search_html)
    list_spu = get_search_spu_ids(search_html)
    list_price = get_price(search_html)
    print(list_ids)
    print(list_spu)
    # # 整理搜索结果数组
    # for i, item in enumerate(list_ids):
    #     try:
    #         if list_spu[i] == "0" or list_spu[i] == "":
    #             list_spu[i] = list_ids[i]
    #     except:
    #         print("结束" + str(i))
    #         break
    # 整理搜索结果数组
    for i, item in enumerate(list_ids):
        try:
            if list_spu[i] == "0" or list_spu[i] == "":
                del list_spu[i]
                del list_ids[i]
        except:
            print("结束" + str(i))
            break
    print(list_ids)
    print(list_spu)
    for i in range(20):
        try:
            print(str(i))
            first_thing_id = list_ids[i]
            first_thing_spu = list_spu[i]

            print('商品id' + first_thing_id)
            print('商品spu' + first_thing_spu)
            thing_html = get_thing_html(first_thing_id)
            thing_price = list_price[i]
            print(str(thing_price))
            thing_pics = get_pics(thing_html)
            thing_info = get_info_pics(first_thing_id, first_thing_spu)
            thing_name = get_name(thing_html)
            insert_sql(thing_name, thing_price, thing_pics, thing_info)
        except:
            print("错误>>>" + i)

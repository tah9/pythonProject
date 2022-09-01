import pymysql
import requests
import re
import selenium

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# 插入全国列车（包含经过站点、时间等信息）

# 连接数据库
connect = pymysql.connect(host="localhost", port=3306, user="root", password="123456++q", database="transport",
                          client_flag=10, charset="utf8mb4")
cursor = connect.cursor()


capa = DesiredCapabilities.CHROME

capa["pageLoadStrategy"] = "none"  # 懒加载模式，不等待页面加载完毕

option = webdriver.ChromeOptions()
# 不加载图片, 提升速度
option.add_argument('blink-settings=imagesEnabled=false')
# 隐藏浏览器
option.add_argument('--headless')
driver = webdriver.Chrome(
    executable_path="C:\Program Files (x86)\Google\chromedriver.exe",
    options=option,
    desired_capabilities=capa)
wait = WebDriverWait(driver, 20)  # 等待的最大时间20s

types = '动车 市郊 快慢 快速 普客 普快 特快 直特 高速'.split(' ')


def getHasStationTableIndex():
    for index in range(len(driver.find_elements_by_class_name('f16'))):
        if '站序' in str(driver.find_elements_by_class_name('f16')[index].text):
            return index


for trainType in types:
    driver.get("https://train.hao86.com/" + trainType + "/")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "clearfix")))
    driver.find_elements_by_class_name('clearfix')
    trainTable = driver.find_elements_by_class_name('clearfix')[5].text
    trainNames = str(trainTable).split('\n')
    for trainId in trainNames:
        driver.get("https://train.hao86.com/"+trainId+"/")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "f16")))
        stationTable = str(driver.find_elements_by_class_name('f16')[getHasStationTableIndex()].text).replace('\n',' ').split(' ')

        stations = '['
        for i in range(8, len(stationTable), 8):
            stationNumber = stationTable[i]
            stationName = stationTable[i+1]
            startTime = stationTable[i+4]
            endTime = stationTable[i+3]
            time = stationTable[i+5]
            arriveDate = stationTable[i+6]
            stopTime = stationTable[i+7]

            stations += ('{"stationNumber":'+stationNumber+',')
            stations += ('"stationName":"'+stationName+'",')
            stations += ('"startTime":"'+startTime+'",')
            stations += ('"endTime":"'+endTime+'",')
            stations += ('"time":"'+time+'",')
            stations += ('"arriveDate":"'+arriveDate+'",')
            stations += ('"stopTime":"'+stopTime+'"},')

        stations = stations[:-1]
        stations += ']'


        # 插入数据库
        sql = "INSERT INTO train (trainId,stations) \
                            VALUE('%s','%s')" \
              % (trainId, stations)
        cursor.execute(sql)
        connect.commit()
        print(trainId+'插入成功')
driver.quit()

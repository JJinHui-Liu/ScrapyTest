import requests
from bs4 import BeautifulSoup
import time
import csv

urlFirst = "https://www.apartments.com/houses/philadelphia-pa/3-bedrooms/"
urlSecond = "/?bb=493w2jw8yHp371oiM"

headers = {
    "Cooie": "obuid=2b129627-e4a4-4afa-9549-8be6abf5a7b0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

i = 0
philyinfo = ['address', 'price', 'type']
houseInfoList = []

for i in range(10):
    print("Start loading page " + str(i + 1) + "...")
    url = urlFirst + str(i + 1) + urlSecond

    # 解析页面
    response = requests.get(url=url, headers=headers)
    # print(response.text)
    page = BeautifulSoup(response.text, "html.parser")

    if i + 1 == 1:
        houseAddress = page.find_all("p", class_="property-address js-url")
        priceList = page.find_all("span", class_="property-rents")
        typeList = page.find_all("span", class_="property-beds")
    else:
        houseAddress = page.find_all("div", class_="property-address js-url")
        priceList = page.find_all("div", class_="price-range")
        typeList = page.find_all("div", class_="bed-range")

    houseAddressList = []
    for x in range(len(houseAddress) - 1):
        if i + 1 == 1:
            if x % 2 == 0:
                house = houseAddress[x].text + " " + houseAddress[x + 1].text
                houseAddressList.append(house)
        else:
            house = houseAddress[x].text
            houseAddressList.append(house)

    for y in range(len(houseAddressList)):
        houseInfo = {
            "address": houseAddressList[y],
            "price": priceList[y].text,
            "type": typeList[y].text
        }
        houseInfoList.append(houseInfo)

    # 防止IP被封
    time.sleep(2)
    print("Page " + str(i + 1) + " Done..." + '\n')

csv_file = 'phily-rent.csv'
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=philyinfo)
        writer.writeheader()
        for data in houseInfoList:
            writer.writerow(data)
        print('All data has written.')
except IOError:
    print("I/O error")

# 确定页数
# def get_page_range(page):
#     pageRange = page.find("span", class_="pageRange")
#     pageNum = pageRange.text[-2:]
#     print(pageNum)
#     return pageNum

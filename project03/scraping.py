from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests


client = MongoClient('52.78.107.146', 27017, username="test", password="test")
db = client.dbsparta_plus_week3

driver = webdriver.Chrome('./chromedriver')

url = "http://matstar.sbs.co.kr/location.html"

driver.get(url)
time.sleep(5)

# 더보기 버튼의 선택자로 버튼 클릭하기
btn_more = driver.find_element_by_css_selector("#foodstar-front-location-curation-more-self > div > button")
btn_more.click() # 더보기 버튼을 클릭해서 12개를 더 가져옴
time.sleep(5)

# 더보기 버튼을 10번 클릭
# for i in range(10):
#     try:
#         btn_more = driver.find_element_by_css_selector("#foodstar-front-location-curation-more-self > div > button")
#         btn_more.click()
#         time.sleep(5)
#     except NoSuchElementException:  # 끝까지 로드해서 더보기 버튼이 없다면
#         break

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')

# 각 식당의 카드
places = soup.select("ul.restaurant_list > div > div > li > div > a")
print(len(places))

# 식당 이름, 주소, 카테고리, 출연 프로그램 및 회차 정보
for place in places:
    title = place.select_one("strong.box_module_title").text
    address = place.select_one("div.box_module_cont > div > div > div.mil_inner_spot > span.il_text").text
    category = place.select_one("div.box_module_cont > div > div > div.mil_inner_kind > span.il_text").text
    show, episode = place.select_one("div.box_module_cont > div > div > div.mil_inner_tv > span.il_text").text.rsplit(" ", 1)
    print(title, address, category, show, episode)

    headers = {
        "X-NCP-APIGW-API-KEY-ID": "9vorxbxcbp",
        "X-NCP-APIGW-API-KEY": "7qOhxgvwOM7NqRIR8w6zQYyVCqIG8yChkUkaZLQq"
    }
    r = requests.get(f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}", headers=headers)
    response = r.json()

    if response["status"] == "OK":
        if len(response["addresses"]) > 0:
            x = float(response["addresses"][0]["x"])    # 문자열 값 -> float으로
            y = float(response["addresses"][0]["y"])
            print(title, address, category, show, episode, x, y)

            # DB에 저장하기
            doc = {
                "title": title,
                "address": address,
                "category": category,
                "show": show,
                "episode": episode,
                "mapx": x,
                "mapy": y}
            db.matjips.insert_one(doc)
        else:
            print(title, "좌표를 찾지 못했습니다")
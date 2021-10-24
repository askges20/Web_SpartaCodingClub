from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep


driver = webdriver.Chrome('./chromedriver')

# 네이버 이미지 검색창 스크래핑
url = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=%EC%95%84%EC%9D%B4%EC%9C%A0"
driver.get(url)
sleep(3)
driver.execute_script("window.scrollTo(0, 1000)")  # 1000픽셀만큼 내리기
sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 맨 아래까지 내리기
sleep(10)

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')
images = soup.select(".tile_item._item ._image._listImage")
print(len(images))

for image in images:
    src = image["src"]
    print(src)


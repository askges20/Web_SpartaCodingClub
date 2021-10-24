from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

driver = webdriver.Chrome('./chromedriver')  # 크롬 드라이버 실행


url = "https://www.melon.com/chart/day/index.htm"
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(url, headers=headers)

driver.get(url)  # 드라이버에 해당 url의 웹페이지 띄우기
sleep(5)  # 페이지가 로딩되는 동안 5초 간 기다리기

req = driver.page_source  # html 정보 가져오기
driver.quit()  # 정보를 가져왔으므로 드라이버 종료

# soup = BeautifulSoup(data.text, 'html.parser')
soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱

songs = soup.select("#frm > div > table > tbody > tr")
print(len(songs))

for song in songs:
    title = song.select_one("td > div > div.wrap_song_info > div.rank01 > span > a").text
    artist = song.select_one("td > div > div.wrap_song_info > div.rank02 > span > a").text
    # likes = song.select_one("td > div > button.like > span.cnt").text
    likes_tag = song.select_one("td > div > button.like > span.cnt")
    likes_tag.span.decompose()  # span 태그 없애기
    likes = likes_tag.text.strip()  # 텍스트화한 후 앞뒤로 빈 칸 지우기
    print(title, artist, likes)



# 동적 웹 페이지를 스크래핑하려면 selenium 필요, 아래 코드는 selenium을 사용하지 않고 requests 이용

# import requests
# from bs4 import BeautifulSoup
#
#
# url = "https://www.melon.com/chart/day/index.htm"
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(url, headers=headers)
#
# req = data.text
# soup = BeautifulSoup(req, 'html.parser')
#
# songs = soup.select("#frm > div > table > tbody > tr")
# print(len(songs))
#
# for song in songs:
#     title = song.select_one("td > div > div.wrap_song_info > div.rank01 > span > a").text
#     artist = song.select_one("td > div > div.wrap_song_info > div.rank02 > span > a").text
#     likes = song.select_one("td > div > button.like > span.cnt").text
#     print(title, artist, likes)
from datetime import datetime

# 1. f-string
name = '홍길동'
age = '30'

# hello = '제 이름은 ' + name + '이구요' # 기존에 쓰던 방식
hello = f'제 이름은 {name}입니다. 나이는 {age}입니다' # f-string
print(hello)


# 2. datetime 함수

today = datetime.now() # 지금 날짜 시간
mytime = today.strftime('%Y-%m-%d-%H-%M-%S') # 원하는 형태로 변환하기
# mytime = today.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')
filename = f'file-{mytime}'
print(mytime)
print(filename)
# selenium 관련 라이브러리를 불러오는 코드
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# 프로그램을 잠깐 멈추게 하기위한 라이브러리
import time
# url로 이미지를 다운받기 위한 라이브러리
import urllib.request

# 다운받은 chromedriver를 불러와서 driver 변수에 저장
driver = webdriver.Chrome(

) 

# driver로 해당 페이지로 이동 : 구글 이미지로 이동
driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")

# 검색창 element 찾기 / 구글 이미지 input name = q
#elem = driver.find_element_by_name("q")
elem = driver.find_element(by="name",value="q")

# 원하는 값 입력
elem.send_keys("횡단보도")

# 입력한 값 전송
elem.send_keys(Keys.RETURN)

SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element(by = 'css selector', value=".my34qd").click()
        except: break
    last_height = new_height

# 내가 필요한 요소 선택 : 검색한 미리보기 이미지
#images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")[0].click()

images = driver.find_elements(by = 'css selector', value=".rg_i.Q4LuWd")
print(len(images))
count = 1
#반복문으로 이미지요소 배열들 돌며 작업 
for image in images:
    # 이미지 클릭
    time.sleep(1)
    image.click()
    # 브라우저가 클릭을 한후 바로 뜨진 않으니 기다리는 시간을 주기 위함
    time.sleep(3)

    # 미리보기 이미지를 클릭해서 큰 이미지를 띄우고 큰 이미지를 선택하고 src 속성을 가져옴
    imgUrl = driver.find_element(by='css selector',value=".r48jcc.pT0Scc.iPVvYb").get_attribute("src")

    # 이미지를 url로 다운받는다.
    urllib.request.urlretrieve(imgUrl, "./imgs/"+str(count)+".jpg")

    count = count + 1

driver.close()
from selenium import webdriver
from bs4 import BeautifulSoup
from hashlib import sha224
# from pprint import pprint

# Checking the fairness of roulette
h = "595fd194a3587442c557e48ac1c555d6bd0b908ccfe8288f72b6adb3"
h_salt = bytes("caebf81a9a784d3c439c0ef575dc7c0ac129b02e35f6c1560261dacf", 'utf-8')
num = bytes("0.273330219852116514546530502237", 'utf-8')
game_hash = sha224(num)
print(game_hash.hexdigest())
salted_hash = sha224(num + h_salt)
print(salted_hash.hexdigest())
print(salted_hash.hexdigest() == h)

# Parsing the roulette page
path_to_driver = "C://Users//Andrey.Zakharov//gdriver//geckodriver.exe"
driver = webdriver.Firefox(executable_path=path_to_driver)
driver.get("https://csgocasino.ru/#game/double")

pageSource = driver.page_source
soup = BeautifulSoup(pageSource, 'html.parser')
# pprint(list(soup.children))
html_main = list(soup.children)[0]
# pprint(list(html_main.children))
html_body = list(html_main.children)[1]
# pprint(list(html_body.children))
wrapper = list(html_body.children)[4]
# pprint(wrapper.prettify())
content = wrapper.find(class_="content")
# pprint(content.prettify())
container = content.find(class_="container")
# pprint(container.prettify())
container_inner = container.find(class_="content-main-inner top-block")
widgets = container_inner.find(class_="top-widgets")
content_inner = widgets.find(class_="content-inner")
game_data = content_inner.find(class_="game bonus-room")
game_content = game_data.find(class_="game-content")
roulette_history = game_content.find(class_="game-roulette-history")
history_list = list(roulette_history.children)[0]
data = []
for child in list(history_list.children):
    data.append(int(child.get_text()))

driver.close()

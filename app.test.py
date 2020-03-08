import json
import requests

from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://localhost:8080/tetris/games/static")
assert "Tetris Games" in driver.title
elem = driver.find_elements_by_css_selector("tr.uk-card")

response = requests.get('http://localhost:8080/tetris/games')
body = json.loads(response.content.decode('utf-8'))
non_zero_games = [game for game in body if game['score'] != 0]

assert len(non_zero_games) == len(elem)-1

driver.close()

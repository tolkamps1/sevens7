import json
import requests

from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://localhost:8080/")
assert "Sevens7 Card Game" in driver.title

driver.close()

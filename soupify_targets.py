from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from selenium import webdriver 
import csv
from collections import defaultdict

sites = []
with open("1 data/2 processed/Networking database.csv","r") as file:
    table = csv.reader(file)
    for row in table:
        sites.append(row)
        
firms = [row[0] for row in sites[1:]]
urls = [row[2] for row in sites[1:]]
targets = {firm:url for firm,url in zip(firms,urls)}

path = r"C:\Windows\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("headless")

def get_site_html(url):
    browser = webdriver.Chrome(executable_path=path,options=options)
    browser.get(url)
    html = browser.page_source
    time.sleep(3)
    soup = BeautifulSoup(html,'html.parser')
    browser.quit()
    return str(soup)
    
soups = defaultdict(str)
for target,url in targets.items():
    print(target)
    if "https" in url:
        soups[target] = get_site_html(url)
    else:
        continue
soups_json = json.dumps(soups)
date_stamp = datetime.now().strftime("%Y%m%d%H%M")
with open(f"{date_stamp} soups.json","w") as file:
    file.write(json.dumps(soups))

import requests
from bs4 import BeautifulSoup
import lxml
import time
import csv
import json
import os

headers = {
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

req = requests.get(url='https://fssp.gov.ru/2738525/', headers=headers)
soup = BeautifulSoup(req.text, 'lxml')
a = soup.find_all('a', class_='b-file_item__link')
print(a)
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
url = input('Введите url сайта, который хотить спарсить: ')

def get_page(url, headers):
    req = requests.get(url=url, headers=headers)
    with open('docs.html', 'w') as file:
        file.write(req.text)

    print('Копия сайта успешно создана!')
    print()
    time.sleep(1)

def get_new_urls_page():
    with open('docs.html') as file:
        src = file.read()

    print('Начало создания копий сайтов опередленных законов!')
    print()
    time.sleep(1)

    soup = BeautifulSoup(src, 'lxml')
    type_of_laws_list = soup.find('ul', class_='c-list').find_all('li')
    title_of_laws_list = []

    for item in type_of_laws_list:
        title_of_laws = item.text.strip()
        title_of_laws_list.append(title_of_laws)
        url_of_laws = item.find('a').get('href')
        req = requests.get(url=url_of_laws, headers=headers)
        with open(f'html_pages\\{title_of_laws}.html', 'w') as file:
            file.write(req.text)

        print(f'Копия сайта {title_of_laws} успешно создана!')
        time.sleep(1)

    return title_of_laws_list

def get_content():
    title_of_laws_list = get_new_urls_page()

    print()
    print('Создаются json и csv файлы!')
    print()
    time.sleep(1)

    result_dict = {}

    for item in title_of_laws_list:
        with open(f'html_pages\\{item}.html') as file:
            src = file.read()

        sub_dict = {}

        soup = BeautifulSoup(src, 'lxml')
        laws_list = soup.find('ul', class_='c-list').find_all('li')
        for law in laws_list:
            title_of_law = law.find('a').text.strip()
            url_of_law = law.find('a').get('href')

            sub_dict[title_of_law] = url_of_law

        result_dict[item] = sub_dict

    with open('data\\result.json', 'w', encoding='utf-8') as file:
        json.dump(result_dict, file, indent=4, ensure_ascii=False)

    print('json файл успешно создан!')
    print()
    time.sleep(1)

    with open('data\\result.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Вид подзаконного акта',
                'Название подзаконного акта',
                'Ссылка на подзаконный акт'
            )
        )

    for key in result_dict:
        for k, v in result_dict[key].items():
            with open('data\\result.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        key,
                        k,
                        v
                    )
                )

    print('csv файл успешно создан!')
    print()
    time.sleep(1)

    return result_dict

def download_pdf_files():
    result_dict = get_content()

    print('Скачиваем pdf файлы законов!')
    print()
    time.sleep(1)

    i = 1
    for key in result_dict:
        j = 1
        os.mkdir(f'data\\{key}')

        for k, v in result_dict[key].items():
            req = requests.get(url=v, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')

            try:
                all_download_urls = soup.find_all('div', class_='c-group-item t-4')
                for item in all_download_urls:
                    pdf_url = item.find('a').get('href')
                    if pdf_url.endswith('pdf'):
                        pdf_req = requests.get(url=pdf_url, headers=headers)

                        with open(f'data\\{key}\\{key}_{j}.pdf', 'wb') as file:
                            file.write(pdf_req.content)
            except:
                print('Нет файлов для скачивания!')

            print(f'{i}) Успешной скачаен файл {key}_{j}')
            j += 1
            i += 1
        j = 1

def main():
    get_page(url, headers)
    download_pdf_files()

if __name__ == '__main__':
    main()


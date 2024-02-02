import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# URL страницы с формой авторизации и страницы с данными после авторизации
login_url = "http://cab2.ru/eng.php"


# куки ебашим
def parserpy():
    data_url = "http://cab2.ru/sched.php"
    saved_cookies = {'PHPSESSID': 'o5328lmjv562nnf89kae6vq0t0', }
    session = requests.Session()
    session.cookies.update(saved_cookies)
    # парсим
    target_response = session.get(data_url)
    html_code = target_response.text
    soup = BeautifulSoup(html_code, 'html.parser')
    # делаем дф
    second_table = soup.find_all('table')[1]
    data = []

    for row in second_table.find_all('tr')[1:]:
        cols = [col.text.strip() for col in row.find_all(['th', 'td'])]
        data.append(cols)

    while True:
        session.cookies.update(saved_cookies)
        new_target_response = session.get(data_url)
        new_html_code = new_target_response.text
        new_soup = BeautifulSoup(new_html_code, 'html.parser')
        new_second_table = new_soup.find_all('table')[1]
        new_data = []

        for new_row in new_second_table.find_all('tr')[1:]:
            new_cols1 = [col.text.strip() for col in new_row.find_all(['th', 'td'])]
            new_data.append(new_cols1)

        if new_data == data:
            print(new_data[1:], 'проходит проверка if')
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)
            time.sleep(5)
            continue

        else:
            print("Данные изменились!")

            # ссылка
            new_data_with_links = []
            for new_row in new_second_table.find_all('tr')[1:]:
                new_cols_with_link = [col.text.strip() for col in new_row.find_all(['th', 'td'])]
                new_link_elem = new_row.find('a')
                if new_link_elem:
                    new_link = new_link_elem['href']
                    new_link_with_prefix = 'http://cab2.ru' + new_link
                    new_cols_with_link.append(new_link_with_prefix)
                new_data_with_links.append(new_cols_with_link)

            new_info = new_data_with_links[1:]
            time.sleep(5)
            return new_info

    print('закончился парсер')
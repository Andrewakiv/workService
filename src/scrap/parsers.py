import requests
from bs4 import BeautifulSoup
from random import randint

headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    },
    {
        "User Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
    }
]


def work(path, city=None, language=None):
    vacancies = []
    errors = []
    if path:
        req = requests.get(path, headers=headers[randint(0, 4)])
        if req.status_code == 200:
            src = req.text
            soup = BeautifulSoup(src, 'lxml')

            lst = soup.find('div', id='pjax-job-list')
            if lst:
                all_vacancies = lst.find_all('div', class_='job-link')

                for i in all_vacancies:
                    title = i.h2.a['title'].rsplit(', ', 1)[0]
                    url = 'https://www.work.ua' + i.h2.a['href']
                    description = ' '.join(i.p.text.split())
                    company = i.find('div', class_='add-top-xs').span.b.text
                    vacancies.append({'title': title, 'url': url, 'description': description, 'company': company,
                                      'city_id': city, 'language_id': language})
            else:
                errors.append({'url': path, 'title': "Div does not exists"})
        else:
            errors.append({'url': path, 'title': "Page do not response"})

    return vacancies, errors


def dou(path, city=None, language=None):
    vacancies = []
    errors = []
    if path:
        req = requests.get(path, headers=headers[randint(0, 4)])
        if req.status_code == 200:
            src = req.text
            soup = BeautifulSoup(src, 'lxml')

            lst = soup.find('ul', class_='lt')
            if lst:
                all_vacancies = lst.find_all('li', class_='l-vacancy')

                for i in all_vacancies:
                    title = i.find('div', class_='title').a.text
                    url = i.find('div', class_='title').a['href']
                    description = ' '.join(i.find('div', class_='sh-info').text.split())
                    company = i.find('div', class_='title').find('a', class_='company').text.strip()
                    vacancies.append({'title': title, 'url': url, 'description': description, 'company': company,
                                      'city_id': city, 'language_id': language})
            else:
                errors.append({'url': path, 'title': "Ul does not exists"})
        else:
            errors.append({'url': path, 'title': "Page do not response"})

    return vacancies, errors


def djinni(path, city=None, language=None):
    vacancies = []
    errors = []
    if path:
        req = requests.get(path, headers=headers[randint(0, 4)])
        if req.status_code == 200:
            src = req.text
            soup = BeautifulSoup(src, 'lxml')

            lst = soup.find('ul', class_='list-unstyled list-jobs mb-4')
            if lst:
                all_vacancies = lst.find_all('li', class_='list-jobs__item job-list__item')

                for i in all_vacancies:
                    company = i.find('a', class_="mr-2").text.strip()
                    title = i.find('div', class_="job-list-item__title mb-1 position-relative d-flex").text.strip()
                    url = 'https://djinni.co' + i.find('div', class_="job-list-item__title mb-1 position-relative d-flex").a['href']
                    desc_short = ' '.join(
                        [j.strip() for j in i.find('div', class_="job-list-item__description").text.split('\n') if len(j) > 0])
                    desc_long = i.find('div', class_="job-list-item__description").span['data-original-text']
                    vacancies.append({'title': title, 'url': url, 'description': desc_short, 'company': company,
                                      'city_id': city, 'language_id': language})
            else:
                errors.append({'url': path, 'title': "Ul does not exists"})
        else:
            errors.append({'url': path, 'title': "Page do not response"})

    return vacancies, errors


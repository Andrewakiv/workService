import asyncio
import json
import os
import sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "work_service.settings"


import django
django.setup()

from django.db import DatabaseError
from scrap.models import City, Language, Vacancy, Url
from scrap import parsers


User = get_user_model()

parse_resources = (
    (parsers.work, 'work'),
    (parsers.dou, 'dou'),
    (parsers.djinni, 'djinni')
)

vacancies = []
errors = []


def get_settings():
    qs = User.objects.filter(send_mail=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url'] = url_dct[pair]
        urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    vacancies.extend(job)


settings = get_settings()
url_list = get_urls(settings)


loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url'][resource], data['city'], data["language"])
             for data in url_list
             for func, resource in parse_resources]
# tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

# for data in url_list:
#     for func, resource in parse_resources:
#         url = data['url'][resource]
#         vacancy, error = func(url, city=data["city"], language=data["language"])
#         vacancies += vacancy
#         errors += error

if tmp_tasks:
    tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
    loop.run_until_complete(tasks)
    loop.close()


for vacancy in vacancies:
    v = Vacancy(**vacancy)
    try:
        v.save()
    except DatabaseError:
        pass


with open("all_vacancies.json", "w", encoding='utf-8') as file:
    json.dump(vacancies, file, indent=4, ensure_ascii=False)

with open("log_parse.json", "w", encoding='utf-8') as file:
    json.dump(errors, file, indent=4, ensure_ascii=False)

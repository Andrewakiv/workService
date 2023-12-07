import json
import os
import sys


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "work_service.settings"


import django
django.setup()

from django.db import DatabaseError
from scrap.models import City, Language, Vacancy
from scrap import parsers

parse_resources = (
    (parsers.work, 'https://www.work.ua/jobs-python/'),
    (parsers.dou, 'https://jobs.dou.ua/vacancies/?category=Python'),
    (parsers.djinni, 'https://djinni.co/jobs/?primary_keyword=Python')
)

city = City.objects.filter(slug='Kyiv').first()
language = Language.objects.filter(slug='Python').first()
vacancies = []
errors = []
for resource, path in parse_resources:
    vacancy, error = resource(path)
    vacancies += vacancy
    errors += error

for vacancy in vacancies:
    v = Vacancy(**vacancy, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass


with open("all_vacancies.json", "w", encoding='utf-8') as file:
    json.dump(vacancies, file, indent=4, ensure_ascii=False)

with open("log_parse.json", "w", encoding='utf-8') as file:
    json.dump(errors, file, indent=4, ensure_ascii=False)

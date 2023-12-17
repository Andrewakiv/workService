import json
import logging
import os
import sys
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
import django

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "work_service.settings"

django.setup()
from scrap.models import City, Language, Vacancy, Url
from work_service.settings import EMAIL_HOST_USER

User = get_user_model()

subject = 'Hot vacancies'
text_content = 'hot vacancies'
from_email = EMAIL_HOST_USER
empty = 'There are not new vacancies for your filters'

qs = User.objects.filter(send_mail=True).values('city', 'language', 'email')
# print('qs', qs)
user_dct = {}
for i in qs:
    user_dct.setdefault((i["city"], i['language']), [])
    user_dct[(i["city"], i['language'])].append(i['email'])
# print("user_dct", user_dct)
if user_dct:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in user_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    # print('params', params)
    qs = Vacancy.objects.filter(**params).values()[:10]
    # print('qs', qs)
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i["city_id"], i['language_id']), [])
        vacancies[(i["city_id"], i['language_id'])].append(i)
    # print("vacancies", vacancies)
    for keys, emails in user_dct.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3><a href="{ row["url"] }">{ row["title"] }</a></h5>'
            html += f"<p>{row['description']}</p>"
            html += f"<p>{row['company']}</p><br><hr>"
        _html = html if html else empty
        # for email in emails:
            # to = email
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(_html, "text/html")
            # msg.send()

qs = Url.objects.all().values('city', 'language')
urls_dct = {(i["city"], i['language']): True for i in qs}

logging.basicConfig(filename='data.log', level=logging.INFO, format='%(message)s')
for keys in user_dct.keys():
    if keys not in urls_dct:
        urls_err = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: There are not url for city: {keys[0]} and language: {keys[1]}'
        logging.info(urls_err)


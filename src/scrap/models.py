from django.db import models
import jsonfield


def default_url():
    return {'work': '', 'dou': '', 'djinni': ''}


class City(models.Model):
    name = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    url = jsonfield.JSONField(default=default_url)
    
    class Meta:
        unique_together = ('city', 'language')
    
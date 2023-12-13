from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


def home_view(request):
    form = FindForm()

    context = {
        'form': form
    }

    return render(request, 'scrap/vacancies/home.html', context=context)


def list_view(request):
    vacancies = Vacancy.objects.all()

    if request.method == 'GET':
        form = FindForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            # print(cd)
            if cd['city'] and cd['language']:
                vacancies = Vacancy.objects.filter(city__name=cd['city'], language__name=cd['language'])
            elif cd['language']:
                vacancies = Vacancy.objects.filter(language__name=cd['language'])
            elif cd['city']:
                vacancies = Vacancy.objects.filter(city__name=cd['city'])
            else:
                vacancies = Vacancy.objects.all()
            # print(vacancies)
    else:
        form = FindForm()

    paginator = Paginator(vacancies, 10)
    page_number = request.GET.get('page', 1)
    vacancies = paginator.page(page_number)

    context = {
        'object_list': vacancies,
        'form': form
    }

    return render(request, 'scrap/vacancies/list.html', context=context)

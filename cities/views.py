from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from cities.models import City
from cities.forms import HtmlForm, CityForm


def home(request):
    """Функція відображення"""
    cities = City.objects.all()
    paginator = Paginator(cities, 4)  # 16,17,18 це пагінатор
    page = request.GET.get('page')
    cities = paginator.get_page(page)
    context = {'objects_list': cities, }
    return render(request, 'cities/home.html', context)


class CityDetailView(DetailView):
    """Деталізація конкретного екземпляру"""
    queryset = City.objects.all()
    context_object_name = 'object'
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Створення міста"""
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'Місто створено!'
    login_url = '/accounts/login/'


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Редагування міста"""
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'Місто відредаговано!'
    login_url = '/accounts/login/'


class CityDeleteView(LoginRequiredMixin, DeleteView):
    """Видалення міста"""
    model = City
    success_url = reverse_lazy('cities:home')
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Місто видалено!')
        return self.post(request, *args, **kwargs)

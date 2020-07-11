from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from cities.models import City
from cities.forms import CityForm


class CityListView(ListView):
    """Список населених пунктів"""
    queryset = City.objects.all()
    context_object_name = 'objects_list'
    template_name = 'cities/list.html'
    paginate_by = 5


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
    success_url = reverse_lazy('cities:list')
    success_message = 'Місто створено!'
    login_url = '/accounts/login/'


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Редагування міста"""
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:list')
    success_message = 'Місто відредаговано!'
    login_url = '/accounts/login/'


class CityDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    """Видалення міста"""
    model = City
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:list')
    success_message = 'Місто видалено!'
    login_url = '/accounts/login/'

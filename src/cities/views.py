from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import City
from .forms import CityForm


def home(request):
    cities = City.objects.all()
    paginator = Paginator(cities, 4)
    page = request.GET.get('page')
    cities = paginator.get_page(page)
    return render(request, 'cities/home.html', {'objects_list': cities})


class CityDetailView(DetailView):
    queryset = City.objects.all()
    context_object_name = 'object'
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Створення міста"""
    login_url = '/login/'
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('city:home')
    success_message = 'Місто створено!'


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Редагування міста"""
    login_url = '/login/'
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('city:home')
    success_message = 'Місто відредаговано!'


class CityDeleteView(LoginRequiredMixin, DeleteView):
    """Видалення міста"""
    login_url = '/login/'
    model = City
    success_url = reverse_lazy('city:home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Місто видалено!')
        return self.post(request, *args, **kwargs)

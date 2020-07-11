from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Train
from .forms import TrainForm


class TrainListView(ListView):
    """Список потягів"""
    queryset = Train.objects.all()
    context_object_name = 'objects_list'
    template_name = 'trains/list.html'
    paginate_by = 5


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Створення потягу"""
    login_url = '/accounts/login/'
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('trains:list')
    success_message = 'Потяг створено!'


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    context_object_name = 'object'
    template_name = 'trains/detail.html'


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Редагування потягу"""
    login_url = '/accounts/login/'
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_url = reverse_lazy('trains:list')
    success_message = 'Потяг відредаговано!'


class TrainDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    """Видалення потягу"""
    model = Train
    template_name = 'trains/delete.html'
    success_url = reverse_lazy('trains:list')
    success_message = 'Потяг видалено!'
    login_url = '/accounts/login/'

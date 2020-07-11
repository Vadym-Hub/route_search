from django.urls import path
from .views import TrainCreateView, TrainDetailView, TrainListView
from .views import TrainUpdateView,  TrainDeleteView


app_name = 'trains'

urlpatterns = [
    path('detail/<int:pk>/', TrainDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', TrainUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TrainDeleteView.as_view(), name='delete'),
    path('add/', TrainCreateView.as_view(), name='add'),
    path('', TrainListView.as_view(), name='list'),
]

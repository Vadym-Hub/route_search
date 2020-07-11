from django.urls import path
from .views import CityCreateView, CityListView
from .views import CityUpdateView, CityDeleteView

app_name = 'cities'

urlpatterns = [
    path('update/<int:pk>/', CityUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete'),
    path('add/', CityCreateView.as_view(), name='add'),
    path('', CityListView.as_view(), name='list')
]

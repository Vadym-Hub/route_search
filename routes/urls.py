from django.urls import path

from routes.views import HomeView, RouteDetailView, RouteListView, add_route, find_routes, RouteDeleteView

apps_name = 'routes'

urlpatterns = [
    path('find/', find_routes, name='find_routes'),
    path('add_route/', add_route, name='add_route'),
    path('list/', RouteListView.as_view(), name='list'),
    path('detail/<int:pk>/', RouteDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', RouteDeleteView.as_view(), name='delete'),
    path('', HomeView.as_view(), name='home'),
]

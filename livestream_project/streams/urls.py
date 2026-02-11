from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/create-stream/', views.create_stream, name='create_stream'),
    path('host/<str:stream_id>/', views.host_stream, name='host_stream'),
    path('watch/<str:stream_id>/', views.watch_stream, name='watch_stream'),
    path('end/<str:stream_id>/', views.end_stream, name='end_stream'),
]

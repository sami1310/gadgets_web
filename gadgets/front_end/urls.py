from django.urls import path
from . import views

app_name = 'front_end'
urlpatterns = [
    path('', views.home_page, name='home_page'),

]

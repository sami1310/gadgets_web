from django.urls import path
from .views import HomeListView

app_name = 'front_end'
urlpatterns = [
    path('', HomeListView.as_view(), name='home_page'),

]

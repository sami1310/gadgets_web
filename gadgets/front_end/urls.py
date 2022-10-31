from django.urls import path
from .views import HomeListView, ProductDetailView

app_name = 'front_end'
urlpatterns = [
    path('', HomeListView.as_view(), name='home_page'),
    path('product/<slug>/', ProductDetailView.as_view(), name='detail')

]

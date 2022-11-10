from django.urls import path
from . import views

app_name = 'front_end'
urlpatterns = [
    path('', views.HomeListView.as_view(), name='home_page'),
    path('product/<slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove-item/<slug>', views.remove_single_item, name='remove_single_item'),
    path('summary', views.OrderSummaryView.as_view(), name='summary'),
    path('shipping_address/', views.ShippingAddressView.as_view(),
         name='shipping_address'),
    path('payment/', views.PaymentView.as_view(), name='payment'),


]

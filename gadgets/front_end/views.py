from django.shortcuts import render
from .models import Item
from django.views.generic import ListView, DetailView
# Create your views here.


# def home_page(request):
#all_item = models.Item.objects.order_by('category')
# context = {
# 'items': all_item,
# }
# return render(request, 'front_end/home_page.html', context=context)

class HomeListView(ListView):
    model = Item
    template_name = 'item_list.html'
    queryset = Item.objects.order_by('category')
    context_object_name = 'item_list'


class ProductDetailView(DetailView):
    model = Item
    template_name = 'front_end/product_detail.html'

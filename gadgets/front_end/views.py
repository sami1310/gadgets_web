from django.shortcuts import render
from .models import Item
# Create your views here.


def home_page(request):
    item = Item.objects.all()
    context = {
        'items': 'item',
    }
    return render(request, 'front_end/home_page.html', context=context)

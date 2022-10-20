from django.shortcuts import render
from . import models
# Create your views here.


def home_page(request):
    all_item = models.Item.objects.all()
    context = {
        'items': all_item,
    }
    return render(request, 'front_end/home_page.html', context=context)

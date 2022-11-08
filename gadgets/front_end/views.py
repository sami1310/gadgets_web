from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Order, OrderItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
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


@login_required(login_url='../accounts/login/')
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    order_q = Order.objects.filter(user=request.user, ordered=False)

    if order_q.exists():
        order = order_q[0]

        if order.items.filter(item_id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item added to the cart")
            return redirect('front_end:summary')

        else:
            order.items.add(order_item)
            messages.info(request, "Item added to the cart")
            return redirect('front_end:summary')

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to the cart")
        return redirect('front_end:summary')


class OrderSummaryView(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        try:
            current_order = Order.objects.get(
                user=self.request.user, ordered=False)
            context = {
                'object': current_order
            }
            return render(self.request, 'front_end/summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have any actiive order")
            return redirect('/')
        return render(self.request, 'front_end/summary.html', context)

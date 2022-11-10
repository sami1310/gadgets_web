from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Order, OrderItem, BillingAddress, Payment
from .forms import ShippingAddressForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import stripe
import random
import string
from django.conf import settings
# Create your views here.


stripe.api_key = settings.SRIPE_SECRET_KEY


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


@login_required(login_url='../accounts/login/')
def remove_single_item(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_q = Order.objects.filter(user=request.user, ordered=False)

    if order_q.exists():
        order = order_q[0]

        if order.items.filter(item_id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)

            messages.info(request, "Item Removed")
            return redirect('front_end:summary')

        else:
            messages.info(request, "Item was not in your cart")
            return redirect('front_end:detail', slug=slug)

    else:
        messages.info(request, "you do not have any order")
        return redirect('front_end:detail', slug=slug)


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


class ShippingAddressView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)
            form = ShippingAddressForm()
            context = {
                'form': form,
                'order': order
            }
            return render(self.request, 'shippingaddress.html', context)
        except ObjectDoesNotExist:
            messages.info(request, "You do not have any active order")
            return redirect('front_end:summary')
        return render(self.request, 'front_end/summary.html', context)

    def post(self, *args, **kwargs):
        form = ShippingAddressForm(self.request.POST or None)
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)
            if form.is_valid():
                house_address = form.cleaned_data.get('house_address')
                post_office = form.cleaned_data.get('post_office')
                city = form.cleaned_data.get('city')
                postal_code = form.cleaned_data.get('postal_code')
                phone_number = form.cleaned_data.get('phone_number')

                billing_address = BillingAddress(
                    user=self.request.user,
                    house_address=house_address,
                    post_office=post_office,
                    city=city,
                    postal_code=postal_code,
                    phone_number=phone_number
                )

                billing_address.save()
                order.billing_address = billing_address
                order.save()

                messages.info(self.request, "Address added to the order!")
                return redirect('front_end:payment')

        except ObjectDoesNotExist:
            messages.info(self.request, "No active order")
            return redirect('front_end:summary')


def create_order_ref():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(
            user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order
            }
            return render(self.request, 'payment.html', context)
        else:
            messages.warning(self.request, 'Please add your shipping address')
            return redirect('front_end:shipping_address')

    def post(self, *args, **kwargs):
        order = Order.objects.get(
            user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.total_price()*100)  # converting poisha to taka

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='bdt',
                source=token,
                description='Payment from Gadgets website!'
            )

            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.total_price()
            payment.save()

            order_items = order.items.all()
            order_items.update(ordered=True)

            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.order_ref = create_order_ref()
            order.save()

            messages.success(
                self.request, 'Your order have been placed successfully ')
            return redirect('/')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect('/')
        except stripe.error.RateLimitError as e:
            messages.warning(self.request, f"{err.get('rate limit error')}")
            return redirect('/')
        except stripe.error.AuthenticationError as e:
            messages.warning(self.request, f"{err.get('Not Authenticated')}")
            return redirect('/')
        except stripe.error.APIConnectionError as e:
            messages.warning(
                self.request, f"{err.get('Network Error.Please Try after some time!')}")
            return redirect('/')
        except stripe.error.StripeError as e:
            messages.warning(
                self.request, f"{err.get('Payment Unsuccessful.Please try again later')}")
            return redirect('/')
        except Exception as e:
            messages.warning(
                self.request, f"{err.get('Ooops!Something went wrong!')}")
            return redirect('/')
        except stripe.error.InvalidRequestError as e:
            messages.warning(self.request, f"{err.get('Invalid parametes')}")
            print('Invalid parametes', e)
            print('The amount is:', amount)
            return redirect('/')


class OrderHistoryView(View, LoginRequiredMixin):
    #model = Order
    #template_name = 'order_history.html'
    # queryset = Order.objects.get(
    # user=request.user, ordered=True)
    #context_object_name = 'order_history'
    def get(self, *args, **kwargs):
        try:
            order_history = Order.objects.filter(
                user=self.request.user, ordered=True).all()
            context = {
                'order_history': order_history
            }
            return render(self.request, 'front_end/order_history.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not placed any order!")
            return redirect('/')
        return render(self.request, 'front_end/order_history.html', context)

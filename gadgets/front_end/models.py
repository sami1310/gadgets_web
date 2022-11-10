from django.db import models
from django.urls import reverse
from gadgets import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


CATEGORY_CHOICES = (
    ('D', 'Desktop'),
    ('L', 'Laptop'),
    ('M', 'Mobile'),
    ('C', 'Camera'),
    ('K', 'Keyboard')
)

LABEL_CHOICES = (
    ('N', 'New'),
    ('S', 'SecondHand')
)


# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=80)
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2)
    discount = models.FloatField(blank=True, null=True)
    description = models.TextField()
    slug = models.SlugField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_discount_percent(self):
        discount_percent = 100-((self.discount*100)/self.price)
        return discount_percent

    def get_item_url(self):
        return reverse('front_end:detail', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart(self):
        return reverse('front_end:add_to_cart', kwargs={
            'slug': self.slug
        })

    def short_title(self):
        return self.title[:13] + '...'


class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} - {self.user} - {self.item.title}"

    def total_item_price(self):
        return self.quantity * self.item.price

    def total_discount_item_price(self):
        return self.quantity * self.item.discount

    def amount_saved(self):
        return self.total_item_price() - self.total_discount_item_price()

    def final_price(self):
        if self.item.discount:
            return self.total_discount_item_price()
        return self.total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    order_ref = models.CharField(max_length=15)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.final_price()
        return total

    def get_order_ref_id(self):
        return self.order_ref


class BillingAddress(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    house_address = models.CharField(max_length=100)
    post_office = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    phone_number = PhoneNumberField(blank=False)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=100)
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}"

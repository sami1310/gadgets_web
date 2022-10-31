from django.db import models
from django.urls import reverse

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

    def get_discount_price(self):
        discount_price = self.price-self.discount
        return discount_price

    def get_item_url(self):
        return reverse('front_end:detail', kwargs={
            'slug': self.slug
        })

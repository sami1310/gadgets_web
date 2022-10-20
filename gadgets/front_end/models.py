from django.db import models


CATEGORY_CHOICES = (
    ('D', 'Desktop'),
    ('L', 'Laptop'),
    ('M', 'Mobile'),
    ('C', 'Camera')
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
    discount = models.FloatField()
    description = models.TextField()
    slug = models.SlugField()
    image = models.ImageField()

    def __str__(self):
        return self.title

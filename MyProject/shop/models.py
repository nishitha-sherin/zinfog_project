from django.db import models

# product models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images',blank=True,default='pic.jpg')
    description = models.TextField()
    review = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name


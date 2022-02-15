from django.db    import models

from  


class Product(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table='products'
    
class ProductGroup(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table='productgroups'

class Image(models.Model):
    name = models.ImageField()        


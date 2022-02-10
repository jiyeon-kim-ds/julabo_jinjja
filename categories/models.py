from django.db    import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table='categories'

class Subcategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table='subcategories'

class CategorySubcategory(models.Model):
    category = models.ForeignKey('category', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('subcategory',on_delete=models.CASCADE)

    class Meta:
        db_table='categorysubcategories'


        


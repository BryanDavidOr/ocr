from django.db import models

# Create your models here.


class Ocr(models.Model):
    image = models.ImageField(upload_to='images/', null=True)
    cedula = models.CharField(max_length=10, null=True)

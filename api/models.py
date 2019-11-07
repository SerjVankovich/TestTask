from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Printer(models.Model):
    name = models.CharField(max_length=150)
    api_key = models.CharField(max_length=150, unique=True)
    check_type = models.CharField(max_length=150)
    point_id = models.IntegerField()


class Check(models.Model):
    printer_id = models.ForeignKey('Printer', on_delete=models.CASCADE)
    type = models.CharField(max_length=150)
    order = JSONField()
    status = models.CharField(max_length=150)
    pdf_file = models.FileField(max_length=150, blank=True)
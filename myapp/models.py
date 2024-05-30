from django.db import models

class Test(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

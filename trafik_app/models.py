from django.db import models

class odberkkv(models.Model):
    ndn = models.CharField(max_length=10, null=True)
    megnevezes = models.CharField(max_length=200, null=True)
    gyarto = models.CharField(max_length=200, null=True)
    kategoria = models.CharField(max_length=200, null=True)
    rendeles = models.IntegerField(null=True)
    raktarkeszlet = models.IntegerField(null=True)
    cikkszam = models.CharField(max_length=200, null=True)
    kv0 = models.IntegerField(null=True)
    kv1 = models.IntegerField(null=True)
    kv2 = models.IntegerField(null=True)
    kv3 = models.IntegerField(null=True)






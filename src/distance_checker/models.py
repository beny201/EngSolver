from django.db import models


class BoltStandard(models.Model):
    title = models.TextField(max_length=50)

    def __str__(self):
        return self.title


class WasherStandard(models.Model):
    title = models.TextField(max_length=50)

    def __str__(self):
        return self.title


class NutStandard(models.Model):
    title = models.TextField(max_length=50)

    def __str__(self):
        return self.title


class Bolt(models.Model):
    name = models.TextField(max_length=50)
    thickness_bolt_head = models.FloatField()
    width_bolt_head = models.FloatField()
    length = models.IntegerField()
    diameter = models.IntegerField()
    thread_length = models.FloatField()
    standard = models.ForeignKey(BoltStandard, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Washer(models.Model):
    name = models.TextField(max_length=50)
    thickness_washer = models.FloatField()
    width_washer = models.FloatField()
    diameter = models.IntegerField()
    standard = models.ForeignKey(WasherStandard, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Nut(models.Model):
    name = models.TextField(max_length=50)
    thickness_nut = models.FloatField()
    width_nut = models.FloatField()
    diameter = models.IntegerField()
    standard = models.ForeignKey(NutStandard, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User
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


class Corner(models.Model):
    name = models.TextField(max_length=50, default="Corner")
    girder_angle = models.FloatField(default=14.5)
    girder_height = models.IntegerField(default=400)
    t_flange_girder = models.IntegerField(default=20)
    column_width = models.IntegerField(default=900)
    t_flange_column = models.IntegerField(default=20)
    t_plate_connection = models.IntegerField(default=20)
    bolt_grade = models.TextField(
        choices=[("8_8", "8.8"), ("10_9", "10.9")], default="8_8"
    )
    bolt_diameter = models.IntegerField(default=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    last_modified_date = models.DateField(auto_now=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        title = f"{self.name} - {self.created_date}"
        return title

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
    case = models.CharField(max_length=50)
    girder_angle = models.FloatField()
    girder_height = models.IntegerField()
    t_flange_girder = models.IntegerField()
    column_width = models.IntegerField()
    t_flange_column = models.IntegerField()
    t_plate_connection = models.IntegerField()
    bolt_grade = models.TextField(choices=[("8_8", "8.8"), ("10_9", "10.9")])
    bolt_diameter = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    distance_top = models.IntegerField(null=True)
    distance_bottom = models.IntegerField(null=True)

    def __str__(self):
        title = f"Corner - {self.case} - {self.created_date}"
        return title


class Ridge(models.Model):
    case = models.CharField(max_length=50)
    left_girder_angle = models.FloatField()
    right_girder_angle = models.FloatField()
    girder_height = models.IntegerField()
    left_t_flange_girder = models.IntegerField()
    right_t_flange_girder = models.IntegerField()
    t_plate_connection = models.IntegerField()
    bolt_grade = models.TextField(choices=[("8_8", "8.8"), ("10_9", "10.9")])
    bolt_diameter = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    distance_left = models.IntegerField(null=True)
    distance_right = models.IntegerField(null=True)

    def __str__(self):
        title = f"Ridge - {self.case} - {self.created_date}"
        return title

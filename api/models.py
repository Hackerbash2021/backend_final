from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    PermissionsMixin,
)

# Create your models here.
class Organization(models.Model):
    org_name = models.CharField(max_length=100)
    accessibility = models.BooleanField(default=False)  # false-public true-private
    class_count = models.IntegerField()
    org_type = models.CharField(max_length=50)


class Admin(models.Model):
    admin_name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)


class OrgClass(models.Model):
    class_code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class Exam(models.Model):
    exam_name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    org_class = models.ForeignKey(OrgClass, on_delete=models.CASCADE)


class Student(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)


class UserClass(models.Model):
    user = models.ForeignKey(Student,on_delete = models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    org_class = models.ForeignKey(OrgClass, on_delete=models.DO_NOTHING)

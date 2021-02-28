from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    PermissionsMixin,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, name, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        name = " ".join(name.split()).title()
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, name, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, name, **extra_fields)

    def create_superuser(self, email, password, name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(email, password, name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.EmailField(max_length=320, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    name = models.CharField(max_length=400)
    phone = models.CharField(max_length=10)

    # photo = ProcessedImageField(
    #     upload_to="photos/%Y/",
    #     processors=[ResizeToFill(400, 400)],
    #     format="JPEG",
    #     options={"quality": 60},
    #     blank=True,
    #     null=True,
    #     default="User.png",
    # )
    objects = UserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        "name",
        # "photo",
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


# Create your models here.
class Organization(models.Model):
    org_name = models.CharField(max_length=100)
    accessibility = models.BooleanField(
        default=False)  # false-public true-private
    class_count = models.IntegerField()
    org_type = models.CharField(max_length=50)


class OrgAdmin(User):
    # password = models.CharField(max_length=30)
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, blank=True, null=True)


class OrgClass(models.Model):
    class_code = models.CharField(max_length=9)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class Exam(models.Model):
    exam_name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    org_class = models.ForeignKey(OrgClass, on_delete=models.CASCADE)


class Student(User):
    # password = models.CharField(max_length=30)
    pass


class UserClass(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    org_class = models.ForeignKey(OrgClass, on_delete=models.DO_NOTHING)

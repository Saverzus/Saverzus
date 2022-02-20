from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.db.models.signals import post_save
from django.dispatch import receiver

from friend.models import FriendList

#создание нового пользователя
#создание супер пользователя
class MyAccountManage(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Нужно указать почту")
        if not username:
            raise ValueError("Нужно указать никнейм")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

#получение пути
def get_profile_image_filepath(self, filename):
	return 'profile_images/' + str(self.pk) + '/profile_image.png'

#дефолт картинка
def get_default_profile_name():
    return "images/avatars/default.png"

class Account(AbstractBaseUser):
    email                    = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                 = models.CharField(max_length=30, unique=True)
    date_joined              = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login               = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin                 = models.BooleanField(default=False)
    is_active                = models.BooleanField(default=True)
    is_staff                 = models.BooleanField(default=False)
    is_superuser             = models.BooleanField(default=False)
    profile_image            = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_name)
    hide_email               = models.BooleanField(default=True)

    objects = MyAccountManage()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    #если название картинки аля jksdqhkjwk, то функция поменяет название на profile_image.png
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_image/{self.pk}/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

@receiver(post_save, sender=Account)
def user_save(sender, instance, **kwargs):
    FriendList.objects.get_or_create(user=instance)
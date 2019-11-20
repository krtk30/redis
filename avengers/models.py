from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.
from utils import choices


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    mode = models.CharField(max_length=1, default='A', choices=choices.MODE)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """
    Inherits BaseUserManager class
    """

    def create_user(self, email, mobile, password=None, username=None, **other_fields):
        """
        Creates and saves a User with the given email, username and password.
        """
        if username is None:
            username = email

        if not email:
            raise ValueError(_('Users must have an email address'))

        if mobile is None:
            raise TypeError('Users must have a mobile number')

        user = self.model(username=username, email=self.normalize_email(email), **other_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(email=self.normalize_email(email))
        user.username = username
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.user_type = 'Admin'
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModel):
    """
        Custom user
        """
    username = models.CharField(db_index=True, max_length=255, unique=True)
    dob = models.DateField(verbose_name=_('Date Of Birth'), null=True, blank=True, help_text=_('Date Of Birth'))
    gender = models.CharField(verbose_name=_('Gender'), choices=choices.GENDER, max_length=6, null=True, blank=True,
                              default='MALE', help_text=_('Gender'))
    photo = models.URLField(verbose_name=_('User Image'), null=True, blank=True)
    user_type = models.CharField(verbose_name=_('Type'), max_length=10, choices=choices.USER_TYPE, default='Prospect')
    email = models.EmailField(verbose_name=_('Email lifeline'), max_length=140, help_text=_('Email @'))
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]


class Hero(AbstractBaseUser, BaseModel):
    user = models.ForeignKey(User, verbose_name=_('User profile'), related_name='users', on_delete=models.CASCADE,
                                null=True, blank=True)
    real_name = models.CharField(verbose_name=_('Real Name'), max_length=140, help_text=_('Real Name'))
    alias = models.CharField(verbose_name=_('Alias Name'), max_length=140, help_text=_('Alias Name'))
    super_powers = models.CharField(verbose_name=_('Super Power'), max_length=140, help_text=_('Super power'))
    mobile = models.CharField(verbose_name=_('CAN BE ACCESSED @'), max_length=140, help_text=_('Can be accessed @'))
    physical_id_marks = models.CharField(verbose_name=_('Physical Identification mark[s]'), max_length=140,
                                         help_text=_('Physical ID marks on body'))
    blood_type = models.CharField(verbose_name=_('Blood type [if any, or alternative requirement]'), max_length=140,
                                  help_text=_('Blood group'))

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.real_name

    class Meta:
        db_table = 'super_hero'
        verbose_name = _('Super Hero')
        verbose_name_plural = _('Super Heroes')
        ordering = ('real_name',)

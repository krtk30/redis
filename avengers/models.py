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


class Hero(BaseModel):
    real_name = models.CharField(verbose_name=_('Real Name'), max_length=140, help_text=_('Real Name'))
    alias = models.CharField(verbose_name=_('Alias Name'), max_length=140, help_text=_('Alias Name'))
    super_powers = models.CharField(verbose_name=_('Super Power'), max_length=140, help_text=_('Super power'))
    mobile = models.CharField(verbose_name=_('CAN BE ACCESSED @'), max_length=140, help_text=_('Can be accessed @'))
    physical_id_marks = models.CharField(verbose_name=_('Physical Identification mark[s]'), max_length=140,
                                         help_text=_('Physical ID marks on body'))
    blood_type = models.CharField(verbose_name=_('Blood type [if any, or alternative requirement]'), max_length=140,
                                  help_text=_('Blood group'))
    email = models.EmailField(verbose_name=_('Email lifeline'), max_length=140, help_text=_('Email @'))

    def __str__(self):
        return self.real_name

    class Meta:
        db_table = 'super_hero'
        verbose_name = _('Super Hero')
        verbose_name_plural = _('Super Heroes')
        ordering = ('real_name',)

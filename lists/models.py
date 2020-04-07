from django.db import models
from django.core.urlresolvers import reverse


class List(models.Model):
    """список"""
    def get_absolute_url(self):
        """получить асолютный url"""
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    """элемент списка"""
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.SET_DEFAULT)

    class Meta:
        unique_together = ('list', 'text')

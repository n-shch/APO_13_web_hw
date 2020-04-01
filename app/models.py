from __future__ import unicode_literals

from datetime import datetime
from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=120, verbose_name=u"Заголовок вопроса")
    text = models.TextField(verbose_name=u"Полное описание вопроса")

    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")

    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']
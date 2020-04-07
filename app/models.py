from __future__ import unicode_literals

import _datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


"""  Создать модели для основных сущностей:
вопрос + , ответ +, тег+, профиль пользователя+,
 лайк. """
# каждому вопросу соответствует свой тег
# каждому тегу соответсвуте тег другой
# каждому вопросу соответсвуте свой вопрос
# юзаем онделит при внешних ссылках

class User(AbstractUser):
    pass

class Tag(models.Model):
    tag_title = models.CharField(max_length=50)
    def __str__(self):
            return self.tag_title

class Question(models.Model):
    question_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=50)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now, verbose_name=u'date published')
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

# модель комментария
class Comment(models.Model):
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now, verbose_name=u'date published')
    def __str__(self):
        return self.comment_text

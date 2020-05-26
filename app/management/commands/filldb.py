from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import *
from random import choice, randint
from faker import Faker
from django.db import IntegrityError

f = Faker()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--profiles', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--comments', type=int)

    def fill_profiles(self, cnt):
        for i in range(cnt):
            try:
                u = User(username=f.name())
                u.save()
                #             Tag.objects.create(tag_title=f.word().lower())
                Profile.objects.create(user=u, nickname=u.username)
            except IntegrityError:
                continue

    def tags(self, cnt):
        for i in range(cnt):
            try:
                Tag.objects.create(tag_title=f.word().lower())
            except IntegrityError:
                continue

    def fill_questions(self, cnt):
        author_ids = list(Profile.objects.all())
        tag_names_list = [tag.tag_title for tag in Tag.objects.all()]
        likes_limit = int(len(author_ids) / 2)
        tags_limit = 10
        for i in range(cnt):
            author_id = f.random.choice(author_ids)
            tags = f.random.sample(tag_names_list, randint(0, tags_limit))
            title = f.sentence(80)[:70]
            text = f.text(400)[:399]
            try:
                question = Question.objects.create_question(
                    author=author_id,
                    title=title,
                    text=text,
                    tag_names=tags)
            except IntegrityError:
                continue
            rating = f.random.randint(-likes_limit, likes_limit)
            is_positive = bool(rating > 0)
            like_authors = f.random.sample(author_ids, abs(rating))
            likes = list()
            for like_author in like_authors:
                Like.objects.create(author=like_author, content_object=question,
                                    is_positive=is_positive)
            question.rating = rating
            question.question_author.save()
            question.save()

    def fill_comments(self, cnt):
        author_ids = list(Profile.objects.all())
        question_ids = list(Question.objects.all())
        for i in range(cnt):
            author_id = f.random.choice(author_ids)
            question_id = f.random.choice(question_ids)
            text = f.text(300)[:200]
            try:
                Comment.objects.create(comment_author=author_id,
                                       question=question_id,
                                       comment_text=text,
                                       )
            except IntegrityError:
                continue

    def handle(self, *args, **options):
        self.fill_profiles(options.get('profiles', 5))
        self.tags(options.get('tags', 10))
        self.fill_questions(options.get('questions', 3))
        self.fill_comments(options.get('comments', 20))


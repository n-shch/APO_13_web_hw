from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, User, Tag, Comment
from random import choice
from faker import Faker

f = Faker()


class Command(BaseCommand):
    def fill_tags(self, cnt):
        for i in range(cnt):
            Tag.objects.create(tag_title=f.word())

#     def add_arguments(self, parser):
#         parser.add_argument('--authors', type=int)
#         parser.add_argument('--questions', type=int)
#         parser.add_argument('--answers', type=int)

    def fill_authors(self, cnt):
        for i in range(cnt):
            u = User(username=f.name())
            u.save()

#             User.objects.create(
#                 rating=f.random_int(min=-100, max=100),
#                 user=u
#             )

    def fill_questions(self, cnt):
        tags_ids = list(Tag.objects.values_list('id', flat=True))
        author_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            Question.objects.create(
                question_author_id=choice(author_ids),
#                 tags.add_arguments(choice(tags_ids)),
                question_text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                question_title=f.sentence()[:128],

            )

    def fill_comments(self, cnt):
            author_ids = list(
                User.objects.values_list(
                    'id', flat=True
                )
            )
            question_ids = list(
                Question.objects.values_list(
                    'id', flat=True
                )
            )

            for i in range(cnt):
                Comment.objects.create(
                    comment_author_id=choice(author_ids),
                    question_id=choice(question_ids),
                    comment_text='. '.join(f.sentences(f.random_int(min=2, max=5))),

                )


    def handle(self, *args, **options):
        self.fill_tags(options.get('tags', 3))
        self.fill_authors(options.get('authors', 4))
        self.fill_questions(options.get('questions', 4))
        self.fill_comments(options.get('comments', 4))
        # self.fill_answers(answers_cnt)

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, LikeQuestion, LikeAnswer, Profile

from faker import Faker
import random

USERS_NUM = 10000
QUESTIONS_NUM = 100000
ANSWERS_NUM = 1000000
TAGS_NUM = 10000
LIKES_NUM = 2000000


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        # self.generate_tags(TAGS_NUM)
        # self.generate_users(USERS_NUM)
        # self.generate_questions(QUESTIONS_NUM)
        # self.generate_answers(ANSWERS_NUM)
        self.generate_rating(LIKES_NUM)
        self.apply_rating()

    def generate_tags(self, count):
        for i in range(count + 1):
            Tag.objects.create(name=self.faker.word())

    def generate_users(self, count):
        for i in range(count + 1):
            username = self.faker.unique.user_name()
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = self.faker.email()
            password = self.faker.password()
            user = User.objects.create(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            Profile.objects.create(user=user)

    def generate_questions(self, count):
        cnt_tags = Tag.objects.all().count()
        tag_id = Tag.objects.order_by('id')[0].id
        min_id = Profile.objects.order_by('id')[0].id
        max_id = Profile.objects.order_by('-id')[0].id
        for i in range(count + 1):
            cnt_tags_q = random.randint(1, 5)
            text = self.faker.paragraph(random.randint(10, 20))
            title = self.faker.paragraph(1)
            profile_id = random.randint(min_id, max_id)
            q = Question.objects.create(
                text=text, title=title, profile_id=profile_id)

            for j in range(cnt_tags_q):
                tag = Tag.objects.get(
                    id=random.randint(tag_id, tag_id + cnt_tags - 1))
                q.tags.add(tag)

    def generate_answers(self, count):
        min_profile_id = Profile.objects.order_by('id')[0].id
        max_profile_id = Profile.objects.order_by('-id')[0].id
        min_question_id = Question.objects.order_by('id')[0].id
        max_question_id = Question.objects.order_by('-id')[0].id
        for i in range(count + 1):
            text = self.faker.paragraph(random.randint(3, 10))
            profile_id = random.randint(min_profile_id, max_profile_id)
            question = random.randint(min_question_id, max_question_id)
            ans = Answer.objects.create(text=text, question_id=question, profile_id=profile_id)

    def generate_rating(self, count):
        min_profile_id = Profile.objects.order_by('id')[0].id
        max_profile_id = Profile.objects.order_by('-id')[0].id
        min_question_id = Question.objects.order_by('id')[0].id
        max_question_id = Question.objects.order_by('-id')[0].id
        for i in range(round(count / 2 + 1)):
            while True:
                like = random.randint(0, 1)
                profile_id = random.randint(min_profile_id, max_profile_id)
                question_id = random.randint(min_question_id, max_question_id)
                if like > 0:
                    like = '1'
                else:
                    like = '-1'
                check = LikeQuestion.objects.filter(
                    question_id=question_id, profile_id=profile_id).count()
                if not check:
                    LikeQuestion.objects.create(
                        question_id=question_id, profile_id=profile_id, mark=like)
                    break

        min_ans_id = Answer.objects.order_by('id')[0].id
        max_ans_id = Answer.objects.order_by('-id')[0].id
        for i in range(round(count / 2 + 1)):
            while True:
                like = random.randint(0, 1)
                profile_id = random.randint(min_profile_id, max_profile_id)
                ans_id = random.randint(min_ans_id, max_ans_id)
                if like > 0:
                    like = '1'
                else:
                    like = '-1'
                check = LikeAnswer.objects.filter(
                    answer_id=ans_id, profile_id=profile_id).count()
                if not check:
                    LikeAnswer.objects.create(
                        answer_id=ans_id, profile_id=profile_id, mark=like)
                    break

    def apply_rating(self):
        for q in Question.objects.all():
            q.rating = 0
            q.save()

        likes_q = LikeQuestion.objects.all()
        for like_q in likes_q:
            question = Question.objects.get(id=like_q.question_id)
            if like_q.mark == 1:
                question.rating += 1
            else:
                question.rating -= 1
            question.save()

        likes_a = LikeAnswer.objects.all()
        for like_a in likes_a:
            answer = Answer.objects.get(id=like_a.answer_id)
            if like_a.mark == 1:
                answer.rating += 1
            else:
                answer.rating -= 1
            answer.save()

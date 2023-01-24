from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-pub_date')

    def hot(self):
        return self.order_by('-rating')

    def get_id(self, id):
        return self.get(id=id)

    def get_tag(self, tag):
        return self.filter(tags__name=tag).order_by('pub_date')


class AnswerManager(models.Manager):
    def by_question(self, id):
        return self.filter(question_id=id).order_by('pub_date')


class TagManager(models.Manager):
    def top(self, count=5):
        return self.annotate(count=Count('questions')).order_by('-count')[:count]


class ProfileManager(models.Manager):
    def top(self, count=5):
        return self.annotate(count=Count('answers')).order_by('-count')[:count]


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(
        'Question', on_delete=models.CASCADE, related_name='answers')

    objects = AnswerManager()


class Tag(models.Model):
    name = models.CharField(max_length=25)

    objects = TagManager()

    def __str__(self):
        return self.name


class LikeQuestion(models.Model):
    MARK = [
        ('1', 'Like'),
        ('-1', 'Dislike'),
    ]
    mark = models.IntegerField(choices=MARK)
    pub_date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="likes")
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)


class LikeAnswer(models.Model):
    MARK = [
        ('1', 'Like'),
        ('-1', 'Dislike'),
    ]
    mark = models.IntegerField(choices=MARK)
    pub_date = models.DateTimeField(auto_now_add=True)
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name="likes")
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=False, related_name='profile')
    avatar = models.ImageField(upload_to='profile_pics/', default='profile_pics/gigachad.jpg')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

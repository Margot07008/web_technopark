# from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum
from django.utils import timezone

from core.models import User

class TagManager(models.Manager):
    pass

class Tag(models.Model):
    objects = TagManager()
    tag_name = models.TextField()

    def __str__(self):
        return self.tag_name


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name=("Голос"), choices=VOTES)
    user = models.ForeignKey(User, verbose_name=("Пользователь"), on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

    def articles(self):
        return self.get_queryset().filter(content_type__model='question').order_by('-create_data')

    def comments(self):
        return self.get_queryset().filter(content_type__model='answer').order_by('-create_data')


class QuestionManager(models.Manager):
    def create_question(self, **kwargs):
        author_id = kwargs['author']
        header = kwargs['header']
        body_quest = kwargs['body_quest']
        # tag =
        question = self.create(author=author_id, header=header, body_quest=body_quest)
        question.save()
        return question


class Question(models.Model):
    objects = QuestionManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    body_quest = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, blank=True)
    total_answers = models.IntegerField(default=0)
    votes = GenericRelation(LikeDislike, related_query_name='question')


    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.header


class AnswerManager(models.Manager):
    def create_answer(self, author, question, body_answer):
        answer = self.create(author=author, question=question, body_answer=body_answer)
        question = Question.objects.get(pk=question.id)
        question.total_answers += 1
        question.save(update_fields=['total_answers'])

        return answer


class Answer(models.Model):
    objects = AnswerManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body_answer = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    votes = GenericRelation(LikeDislike, related_query_name='answer')
    flag = models.BooleanField(blank=True, default=False)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.body_answer

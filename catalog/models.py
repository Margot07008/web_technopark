from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from core.models import User

class TagManager(models.Manager):

    def add_tags(self, tag):
        if Tag.objects.filter(tag_name=tag).exists():
            tag = self.get(tag_name=tag)
            tag.total += 1
            tag.save(update_fields=['total'])
        else:
            tag = self.create(tag_name=tag)
            tag.save()
        return tag



class Tag(models.Model):
    objects = TagManager()
    tag_name = models.TextField()
    total = models.IntegerField(default=1)

    def __str__(self):
        return self.tag_name


class LikeDislikeManager(models.Manager):
    pass

class LikeDislike(models.Model):
    objects = LikeDislikeManager()
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )
    vote = models.SmallIntegerField(choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #ContentType фреймворк
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    obj = GenericForeignKey('content_type', 'object_id')


class QuestionManager(models.Manager):
    def create_question(self, **kwargs):
        author_id = kwargs['author']
        header = kwargs['header']
        body_quest = kwargs['body_quest']
        tags = kwargs['tags']
        question = self.create(author=author_id, header=header, body_quest=body_quest)
        question.save()
        for tag in tags:
            current_tag = Tag.objects.add_tags(tag)
            question.tags.add(current_tag)
        return question


class Question(models.Model):
    objects = QuestionManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    body_quest = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
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

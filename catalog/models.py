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
    def is_liked(self, user, object_id):
        return self.filter(object_id=object_id, user=user,is_active=True).exists()

    def create_like(self, user, instance, object_id, action='up-vote'):
        try:
            like = self.filter(user=user).get(object_id=object_id)
            if like.is_active and action == 'down-vote':
                print("dislike")
                like.is_active = False
                instance.total_likes -= 1
                if instance.total_likes == -1:
                    instance.total_likes = 0
            elif not like.is_active and action == 'up-vote':
                print("like")
                print(instance.total_likes)
                like.is_active = True
                instance.total_likes += 1
            like.save(update_fields=['is_active'])
        except:
            like = self.create(user=user, obj=instance, object_id=instance.id)
            if action == 'up-vote':
                like.is_active = True
                print("create-like")
                print(instance.total_likes)
                instance.total_likes += 1
            else:
                print("create-dislike")
            like.save()

        instance.save(update_fields=['total_likes'])
        return like

class LikeDislike(models.Model):
    objects = LikeDislikeManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    obj = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.user

class QuestionManager(models.Manager):
    def create_question(self, author, header, body_quest, tags):
        question = self.create(author=author, header=header, body_quest=body_quest)
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
    total_likes = models.IntegerField(default=0)

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
        question.save()

        return answer




class Answer(models.Model):
    objects = AnswerManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body_answer = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    total_likes = models.IntegerField(default=0)
    flag = models.BooleanField(blank=True, default=False)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.body_answer

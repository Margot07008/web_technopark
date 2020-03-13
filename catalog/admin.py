from django.contrib import admin

from .models import UserProfile, Answer, Tag, Question

admin.site.register(Tag)
# admin.site.register(Question)
admin.site.register(UserProfile)
admin.site.register(Answer)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'header')
    filter_horizontal = ('tag', )
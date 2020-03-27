from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Answer, Tag, Question

admin.site.register(Tag)
# admin.site.register(Question)
admin.site.register(User, UserAdmin)
admin.site.register(Answer)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'header')
    filter_horizontal = ('tag', )
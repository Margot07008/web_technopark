def users_processors(request):
    from catalog.models import User
    from catalog.models import Tag
    return {'users': User.objects.all(), 'tags': Tag.objects.all()}

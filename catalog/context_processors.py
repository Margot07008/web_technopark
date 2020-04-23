def users_processors(request):
    from catalog.models import User, Tag
    return {'users': User.objects.order_by('-date_joined')[:10], 'tags': Tag.objects.all().order_by('-total')[:10]}

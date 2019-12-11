from django.shortcuts import render


from celeryman import models


def index(request):
    context = {
        "authors": models.Author.objects.all()
    }
    return render(request, 'celeryman/body.html', context)

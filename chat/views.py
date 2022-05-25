from django.shortcuts import render
from django.views.generic import TemplateView

from django.db.models.signals import post_save
from .models import Message


# Create your views here.
def index(request):
    # rooms = Room.objects.all()
    # context = {'rooms': rooms}
    # return render(request, 'chat/index.html', context)
    return render(request, 'chat/index.html')


def room(request):
    return render(request, 'chat/stream.html')


def send_message(sender, instance, created, **kwargs):
    while True:
        if created:
            message = instance.message
            yield "data: %s \n" % message


class DevSSETemplate(TemplateView):
    template_name = "chat/stream.html"


post_save.connect(send_message, sender=Message)

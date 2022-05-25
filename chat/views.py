from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import Message, Room

import time


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
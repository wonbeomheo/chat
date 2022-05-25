from django.db import models
from django.db.models.signals import post_save, pre_save
from users.models import User


# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=200)
    members = models.ForeignKey(User, on_delete=models.CASCADE)


class Message(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    # timestamp = models.DateTimeField()
    # is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message


def save_message(sender, instance, **kwargs):
    # get signal -> send response to all users with the new message
    print("something")


post_save.connect(save_message, sender=Message)
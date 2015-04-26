from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserMessage(models.Model):
	def __unicode__(self):
		return self.user

	user = models.ForeignKey(User)
	intro = models.CharField(max_length=255, default='')
	head = models.CharField(max_length=255, default='default')

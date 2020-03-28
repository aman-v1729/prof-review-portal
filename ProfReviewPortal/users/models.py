from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	rp = models.IntegerField(default = 0)
	warn_offensive = models.BooleanField(default = False)
	def __str__(self):
		return f'{self.user}'

class Ban(models.Model):
	email = models.EmailField(unique = True)
#	start = models.DateTimeField(auto_now_add = True)
#	duration = models.IntegerField()
	end = models.DateTimeField(null = True)
	permanent = models.BooleanField()

	def __str__(self):
		return f'{self.email}'
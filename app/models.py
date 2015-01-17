from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
	user = models.ForeignKey(User, unique=True)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.EmailField(max_length=254, unique=True)
	education = models.CharField(max_length=500, blank=True)
	linkedin = models.URLField(blank=True)

	def __str__(self):
		return self.first_name + " " + self.last_name
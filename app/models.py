from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class Person(models.Model):
	user = models.ForeignKey(User, unique=True)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.EmailField(max_length=254, unique=True)
	education = models.CharField(max_length=500, blank=True)
	linkedin = models.URLField(blank=True)

	def __str__(self):
		return self.first_name + " " + self.last_name

class Problem(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=500, blank=False)
	description = models.TextField(blank=False)
	location = models.CharField(max_length=200, blank=False)
	#latitude = models.FloatField()
	#longitude = models.FloatField()

	def __str__(self):
		return self.title

class ProblemImage(models.Model):
	image = models.ImageField(upload_to="img/", null=True, blank=True)
	problem = models.ForeignKey(Problem)

class ProblemImageForm(ModelForm):
	class Meta:
		model = ProblemImage
		fields = ['image', 'problem']

class Solution(models.Model):
	user = models.ForeignKey(User)
	text = models.TextField()
	vote = models.IntegerField()
	problem = models.ForeignKey(Problem)

	def __str__(self):
		return self.text

class Comment(models.Model):
	user = models.ForeignKey(User)
	text = models.TextField()
	solution = models.ForeignKey(Solution)

	def __str__(self):
		return self.text
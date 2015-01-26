

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
	location = models.CharField(max_length=200, blank=True)
	latitude = models.FloatField(default="40.7127837")
	longitude = models.FloatField(default="-74.0059413")

	def getFullName(self):
		return self.first_name + " " + self.last_name

	def __str__(self):
		return self.first_name + " " + self.last_name

class Skill(models.Model):
	text = models.CharField(max_length=200)
	person = models.ForeignKey(Person)

	def __str__(self):
		return self.text

class Problem(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=500, blank=False)
	description = models.TextField(blank=False)
	location = models.CharField(max_length=200, blank=False)
	latitude = models.FloatField(default="40.7127837")
	longitude = models.FloatField(default="-74.0059413")
	#CATEGORY = (('P','Pollution'),('Poverty','Poverty'),('First World Problems','First World Problems'),('Basic Necessities','Basic Necessities'),('Environment','Environment'),('Human rights','human rights'),('social','social'))
	tags = models.CharField(max_length=100, default='Poverty')
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
	problem = models.ForeignKey(Problem)
	followup = models.ForeignKey('self', default=0, null=True, blank=True)
	upvotes = models.IntegerField()
	text = models.TextField()

	def __str__(self):
		return self.text

#class Project(models.Model):
#        founder = models.ForeignKey(User)
#        problem = models.ForeignKey(Problem)
#        upvotes = models.IntegerField()

 #       def __str__(self):
 #               return self.text
	
#class Project_Comment(models.Model):
 #       user = models.ForeignKey(User)
  #      project = models.ForeignKey(Project)
   #     upvotes = models.IntegerField()
    #    text = models.TextField()
#
 #       def __str__(self):
  #              return self.text


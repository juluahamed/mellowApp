from django.db import models
from django.contrib.auth.models import User

# Declaring Models 
class Category(models.Model):
	name = models.CharField(max_length=50)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	time_created = models.DateTimeField(auto_now_add=True, editable=False)
	time_updated = models.DateTimeField(auto_now=True)
	
	def __unicode__(self): # For Python 2
		return self.name

	def __str__(self):
		return self.name
	
	
class Task(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(max_length=300, default='')
	order = models.IntegerField(default=0)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	time_created = models.DateTimeField(auto_now_add=True, editable=False)
	time_updated = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name
	
	

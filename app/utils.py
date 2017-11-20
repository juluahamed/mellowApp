from django.shortcuts import render, redirect
from functools import wraps
from django.http import Http404
from app.models import Task, Category
from django.contrib.auth.models import User

def user_owns_category(func):
	"""Checks if the logged in user owns the catagory """
	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			category = Category.objects.get(id=kwargs['id'])
		except Category.DoesNotExist:
			raise Http404("This category does not exsist")
		if category.user_id.id == args[0].user.id:
			print('successful')
			return func(*args, **kwargs)
		else:
			return redirect('/')
	return wrapper

def user_owns_task(func):
	""" Checks if the logged in user owns the task"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			category = Category.objects.get(id=kwargs['c_id'])
		except Category.DoesNotExist:
			raise Http404("This category does not exsist")
		try:
			task = Task.objects.get(id=kwargs['t_id'])
		except Task.DoesNotExist:
			raise Http404("This task does not exsist")
		if category.user_id == task.user_id == args[0].user:
			if task.category == category:
				return func(*args, **kwargs)
			else:
				return redirect('/')
		else:
			return redirect('/')
	return wrapper

def order_maintainer(request, original_category, original_order):
	""" Maintains the order when a task is deleted or is shifted to different category """
	temp_original = Task.objects.filter(category=original_category,
				 user_id= User.objects.get(username=request.user.username)).order_by('order')
	for task in temp_original:
		print(task)
		if task.order > original_order:
			task.order -= 1
			task.save()

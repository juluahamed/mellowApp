from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Category, Task
from django.http import JsonResponse
from app.forms import *
from app.utils import user_owns_category, user_owns_task, order_maintainer
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db.models import Max
import json

@login_required
def home(request):
	""" View for root of the site """
	categories = Category.objects.filter(user_id=request.user.id)
	return render(request, 'home.html', {'categories': categories})

@login_required
@user_owns_category
def viewCategory(request, id=None):
	""" Recieves the catagory id and load the tasks for GET request """
	return render(request, 'viewCategory.html', {'cat_id': id})

@login_required
def newCategory(request):
	""" Creates new category"""
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = CategoryForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			if Category.objects.filter(name=form.cleaned_data['name']):
				form = CategoryForm()
				form.custom_error = 'This category name already exsists.'
				return render(request, 'newCategory.html', {'form': form})
			instance = Category(name=form.cleaned_data['name'], user_id= User.objects.get(username=request.user.username))
			instance.save()
			return redirect(home)
		else:
			return redirect(home)

		# if a GET (or any other method) we'll create a blank form
	else:
		form = CategoryForm()
		return render(request, 'newCategory.html', {'form': form})

@login_required
@user_owns_category
def deleteCategory(request, id=None):
	if request.method == 'POST':
		category = Category.objects.get(id=id)
		category.delete()
		return redirect(home)
	else:
		cat = Category.objects.get(id=id)
		return render(request, 'deleteCategory.html', {'cat_name': cat.name, 'cat_id': cat.id})

@login_required
def newTask(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = TaskForm(data=request.POST, user=request.user)
		# check whether it's valid:
		if form.is_valid():
			temp_ord = Task.objects.filter(category=form.cleaned_data['category'],
				 user_id= User.objects.get(username=request.user.username)).aggregate(Max('order'))
			if temp_ord['order__max']  is None:
				temp_ord['order__max'] = 0
			instance = Task(name=form.cleaned_data['name'], description=form.cleaned_data['description'],
				category=form.cleaned_data['category'],
				user_id= User.objects.get(username=request.user.username), order= temp_ord['order__max'] + 1)
			instance.save()
			return redirect(home)
		else:
			return redirect(home)

		# if a GET (or any other method) we'll create a blank form
	else:
		form = TaskForm(user=request.user)
		return render(request, 'newTask.html', {'form': form})

@login_required
@user_owns_task
def editTasks(request, c_id=None, t_id=None):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = TaskForm(data=request.POST, user=request.user)
		# check whether it's valid:
		if form.is_valid():
			instance = Task.objects.get(id=t_id)
			original_category = instance.category
			original_order = instance.order
			if not instance.category == form.cleaned_data['category']:
				temp_ord = Task.objects.filter(category=form.cleaned_data['category'],
				 user_id= User.objects.get(username=request.user.username)).aggregate(Max('order'))
				if temp_ord['order__max']  is None:
					temp_ord['order__max'] = 0
				instance.order = temp_ord['order__max'] + 1
				order_maintainer(request, original_category, original_order)
			instance.name = form.cleaned_data['name']
			instance.description = form.cleaned_data['description']
			instance.category = form.cleaned_data['category']
			instance.save()
			return redirect(home)
		else:
			return redirect(home)

		# if a GET (or any other method) we'll create a blank form
	else:
		task = Task.objects.get(id=t_id)
		form = TaskForm(initial={'name': task.name, 'description': task.description, 'category': task.category}, user=request.user)
		return render(request, 'newTask.html', {'form': form})

@login_required
@user_owns_task
def deleteTasks(request, c_id=None, t_id=None):
	if request.method == 'POST':
		task = Task.objects.get(id=t_id)
		original_category = task.category
		original_order = task.order
		task.delete()
		order_maintainer(request, original_category, original_order)
		return redirect(home)
	else:
		task_ = Task.objects.get(id=t_id)
		return render(request, 'deleteTask.html', {'task_name': task_.name, 'task_id': task_.id, 'c_id': c_id})



@login_required
@user_owns_category
def getTasks(request, id = None):
	""" GET gets all the tasks.
		POST shuffles the priority/order of the tasks"""
	data = []
	if request.method == "POST":
		target_id = request.POST.get('target')
		source_id = request.POST.get('source')
		try:			
			target_task = Task.objects.get(id=target_id)
			source_task = Task.objects.get(id=source_id)
			temp_target = target_task.order
			target_task.order = source_task.order
			source_task.order = temp_target
			target_task.save()
			source_task.save()
		except:
			data.append({"status": 'Error'})
			return JsonResponse(data, safe=False)
		data.append({"status": 'OK'})
		return JsonResponse(data, safe=False)
	
	if id:
		try:
			category = Category.objects.get(id=id)
		except Category.DoesNotExist:
			raise Http404("This category does not exsist")
		tasks = Task.objects.filter(category= category.id, user_id=request.user).order_by('order')
		for task in tasks:
			data.append({"id":task.id, "name":task.name,"description":task.description, "order":task.order})
		return JsonResponse(data, safe=False)



def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
            	password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
            return redirect(home)
    form = RegistrationForm()
    return render(request,'registration/register.html',{'form': form})







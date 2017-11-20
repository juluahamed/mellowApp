from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<id>[0-9]+)/view', views.viewCategory, name='viewcategory'),
    url(r'^(?P<id>[0-9]+)/delete', views.deleteCategory, name='deletecategory'),
    url(r'^task/new', views.newTask, name='newtask'),
    url(r'^(?P<c_id>[0-9]+)/task/(?P<t_id>[0-9]+)/edit', views.editTasks, name='edittask'),
    url(r'^(?P<c_id>[0-9]+)/task/(?P<t_id>[0-9]+)/delete', views.deleteTasks, name='deletetask'),
    url(r'^gettasks/(?P<id>[0-9]+)', views.getTasks, name='gettasks'),
    url(r'^new', views.newCategory, name='newcategory')
    ]
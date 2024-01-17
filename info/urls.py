from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *



urlpatterns = [
    path('',views.index, name='index'),
    path('access-denied/', views.access_denied, name='access_denied'),
    
    path('initialize_days_of_week/', views.initialize_days_of_week, name='initialize_days_of_week'),
    path('get_departments/', views.get_departments, name='get_departments'),

    path('days/', views.DaysList, name='days'),
    path('add_days/', views.AddDays, name='add_days'),
    path('edit_days/<int:pk>/', views.EditDays, name='edit_days'),
    path('delete_days/<int:pk>/', views.DeleteDays, name='delete_days'),

    path('departments/', views.DepartmentList, name='departments'),
    path('add_department/', views.AddDepartment, name='add_department'),
    path('edit_department/<int:pk>/', views.EditDepartment, name='edit_department'),
    path('delete_department/<int:pk>/', views.DeleteDepartment, name='delete_department'),

    path('users/', views.UserList, name = 'userlist'),
    path('toggle_user_active_status/<int:user_id>/', views.toggle_user_active_status, name='toggle_user_active_status'),
    path('users/add', views.AddUser, name='useradd'),
    path('users/edit/<int:id>/', views.EditUser, name = 'useredit'),
    path('users/delete/<int:id>/', views.DeleteUser, name = 'userdelete'),
    
    path('bus/shuttles/', views.ShuttleBus, name = 'shuttle_bus'),

    path('tags/', views.TagList, name = 'tags'),
    path('add_tag/', views.AddTag, name='add_tag'),
    path('edit_tag/<int:pk>/', views.EditTag, name='edit_tag'),
    path('delete_tag/<int:pk>/', views.DeleteTag, name='delete_tag'),

    path('news/', views.NewsList, name='news'),
    path('news/create/', views.AddNews, name='add_news'),
    path('news/edit/<int:news_id>/', views.EditNews, name='edit_news'),
    path('news/delete/<int:id>/', views.DeleteNews, name = 'delete_news'),

    path('notices/', views.NoticeList, name = 'notices'),
    path('notices/add', views.AddNotice, name='addnotice'),

    
]





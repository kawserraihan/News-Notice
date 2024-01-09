from django.urls import path, include
import apis.views as api_view
from django.contrib import admin
from apis import views
from django.urls import resolve

urlpatterns = [ 
    
    path('news/', api_view.NewsAll.as_view()),
    
    
]
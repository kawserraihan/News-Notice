import json
import logging
from django.shortcuts import render
from urllib3 import request
from info.models import *
from .forms import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views import View
import re
from django.views.decorators.http import require_POST

from django.contrib.auth import get_user_model

User = get_user_model

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

#---------------------------------------------------------------------------------------------
#-------------------------------------------Index---------------------------------------------
#---------------------------------------------------------------------------------------------

def access_denied(request):
    return HttpResponseForbidden("Access Denied: You do not have permission to access this page.")

@login_required
def index(request):

    if request.user.is_superuser or request.user.is_active:
        return render(request, 'index.html')

    else:
        message = "You do not have access"
    
    response_data = {'message': message}
    return JsonResponse(response_data)
        


#---------------------------------------------------------------------------------------------
#--------------------------------------Login USER handling------------------------------------  
#--------------------------------------------------------------------------------------------- 



# def login_view(request):
#     user = request.user

#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)

#         if user.is_superuser or user.is_active:
#             return render(request, 'index.html')
        
#         else:

#             context = {'username_incorrect': True}
#             return access_denied
        
#     return access_denied




#------------------------------------------------------------------------------------------------------
#-----------------Runs Only Once In A New Database When There Are No Days In The Database-----------------
#-------------------------------------------Specially Used For Buses-----------------------------------




@login_required
def initialize_days_of_week(request):
    
    # Check if the days of the week have already been added
    if Day.objects.count() == 0:
        days_of_week = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        for day in days_of_week:
           Day.objects.create(day=day)
        
        message = "Days of the week have been added to the BusDay model."
   
    else:
        
        message = "Days of the week have already been added to the BusDay model."

    response_data = {'message': message}
    
    return JsonResponse(response_data)




#---------------------------------------------------------------------------------------------
#-------------------------------------Department List-----------------------------------------
#---------------------------------------------------------------------------------------------





@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def DepartmentList(request):
    
    # Your view logic here
    departmentlist = Department.objects.all()
    form = DepartmentForm()

    context = {
        'departments': departmentlist,
        'form': form
    }

    return render(request, 'coredata/list/departmentlist.html', context)



#---------------------------------------------------------------------------------------------
#------------------------------------- Add Department ----------------------------------------
#---------------------------------------------------------------------------------------------



@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def AddDepartment(request):
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        
        if form.is_valid():
            form.save()  
            
            return redirect('departments')  
        else:
            errors = form.errors
            return JsonResponse({'success': False, 'errors': errors})
    
    else:
        # Log the request method to help diagnose the issue
        print(f"Received a {request.method} request instead of a POST request.")
        return HttpResponseBadRequest("Invalid Request")
    


#---------------------------------------------------------------------------------------------
#-------------------------------------Edit Department ----------------------------------------
#---------------------------------------------------------------------------------------------

@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def EditDepartment(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.save()
        return redirect('departments') 
        
    else:
        print(f"Received a {request.method} request instead of a POST request.")
        return HttpResponseBadRequest("Invalid Request")
    


#---------------------------------------------------------------------------------------------
#-------------------------------------Delete Department --------------------------------------
#---------------------------------------------------------------------------------------------


@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def DeleteDepartment(request, pk):
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.delete()
        return redirect('departments')

    else:
        print(f"Received a {request.method} request instead of a POST request.")
        return HttpResponseBadRequest("Invalid Request")


#---------------------------------------------------------------------------------------------
#--------------------------------Get Department From Anywhere --------------------------------
#---------------------------------------------------------------------------------------------

def get_departments(request):
    departments = Department.objects.all()
    departments_options = '<option value="">Select a Department</option>'
    for depts in departments:
        departments_options += f'<option value="{depts.id}">{depts.name}</option>'
    return JsonResponse(departments_options, safe=False)


#---------------------------------------------------------------------------------------------
#--------------------------------------Days List ---------------------------------------------
#---------------------------------------------------------------------------------------------

@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def DaysList(request):
    
    # Your view logic here
    daylist = Day.objects.all()
    form = DayForm()

    context = {
        'days': daylist,
        'form': form
    }

    return (render(request, 'coredata/list/dayslist.html', context))


#---------------------------------------------------------------------------------------------
#--------------------------------------Add Days-----------------------------------------------
#---------------------------------------------------------------------------------------------

@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def AddDays(request):
    
    if request.method == 'POST':
        form = DayForm(request.POST)
        
        if form.is_valid():
            form.save()
        
            return redirect('days')  

        else:
            errors = form.errors
            return JsonResponse({'success': False, 'errors': errors})
    
    else:
        # Log the request method to help diagnose the issue
        print(f"Received a {request.method} request instead of a POST request.")
        return HttpResponseBadRequest("Invalid Request")
    

#---------------------------------------------------------------------------------------------
#-------------------------------------- Edit Days --------------------------------------------
#---------------------------------------------------------------------------------------------

@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def EditDays(request, pk):
    day = get_object_or_404(Day, pk=pk)

    if request.method == 'POST':
        day.day = request.POST.get('day')
        day.save()
        return redirect('days') 
        
    else:
        print(f"Received a {request.method} request instead of a POST request.")
        return HttpResponseBadRequest("Invalid Request")


#---------------------------------------------------------------------------------------------
#-------------------------------------- Delete Days --------------------------------------------
#---------------------------------------------------------------------------------------------

@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def DeleteDays(request, pk):
    day = get_object_or_404(Day, pk=pk)
    
    if request.method == 'POST':
        day.delete()
        return redirect('days')

    else:
        print(f"Received a {request.method} request instead of a POST request.")
        return HttpResponseBadRequest("Invalid Request")
    

#---------------------------------------------------------------------------------------------
#------------------------------------------- User List ---------------------------------------
#---------------------------------------------------------------------------------------------


@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def UserList(request):
    users = CustomUser.objects.all()
    return render(request, 'coredata/list/userlist.html', {'users': users})


def toggle_user_active_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    is_active = request.POST.get('is_active') == 'on'

    user.is_active = is_active
    user.save()

    # You can customize the response based on your needs
    response_data = {'status': 'success', 'is_active': user.is_active}
    return JsonResponse(response_data)

#---------------------------------------------------------------------------------------------
#------------------------------------------- Add User  ---------------------------------------
#---------------------------------------------------------------------------------------------


logger = logging.getLogger(__name__)
@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def AddUser(request):
    try:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'User added successfully.')
                # Provide the redirect URL in the JsonResponse
                return redirect('userlist')
            else:
                # Return a JsonResponse with the form errors
                return JsonResponse('errors')
        else:
            form = CustomUserCreationForm()
    except Exception as e:
        logger.error(f"An error occurred while adding an user")
        messages.error(request, 'An error occurred while processing your request. Please try again later.')

    # Render the HTML page for the initial GET request
    return render(request, 'coredata/add/useradd.html', {'form': form})


#---------------------------------------------------------------------------------------------
#------------------------------------------ Edit User ----------------------------------------
#---------------------------------------------------------------------------------------------


@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def EditUser(request, id):
    user_to_edit = get_object_or_404(CustomUser, pk=id)

    if request.user.is_superuser:  # Ensure that the logged-in user is a superuser
        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, instance=user_to_edit)
            if form.is_valid():
                # Update user information
                form.save()

                # Update password only if a new password is provided
                password = form.cleaned_data['password']
                if password:
                    user_to_edit.set_password(password)
                    user_to_edit.save()

                return redirect('userlist')  
        else:
            form = CustomUserChangeForm(instance=user_to_edit)

        return render(request, 'coredata/edit/useredit.html', {'form': form, 'users': user_to_edit})
    else:
        # Non-superusers should not be able to edit other users
        return HttpResponseForbidden("You do not have permission to edit this user.")
    

#---------------------------------------------------------------------------------------------
#------------------------------------------ Delete User --------------------------------------
#---------------------------------------------------------------------------------------------


@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def DeleteUser(request, id):
    user = get_object_or_404(CustomUser, pk=id)

    if request.method == 'POST':
        user.delete()
        return redirect('userlist')

    else:
        print(f"Received a {request.method} request instead of a POST request.")
        return HttpResponseBadRequest("Invalid Request")
    


#---------------------------------------------------------------------------------------------
#------------------------------------------ Shuttle Bus --------------------------------------
#---------------------------------------------------------------------------------------------


@login_required

def ShuttleBus(request):
        
    if request.method == 'POST':
        try:
            # Retrieve data from the POST request
            day = request.POST.get('day')
            route_type = request.POST.get('route_type')
            time = request.POST.get('time')
            bus_no = request.POST.get('bus_no')

            # Convert JSON strings to Python lists
            time_list = json.loads(time)
            bus_no_list = json.loads(bus_no)

            # Assuming 'ShuttleSchedule' is your model
            for i in range(min(len(time_list), len(bus_no_list))):
                schedule = BusSchedule(day=day, route_type=route_type, time=time_list[i], bus_no=bus_no_list[i])
                schedule.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return render(request, 'modules/shuttle-bus.html')



#---------------------------------------------------------------------------------------------
#------------------------------------------ Tags ---------------------------------------------
#---------------------------------------------------------------------------------------------



@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def TagList(request):
    
    # Your view logic here
    taglist = Tag.objects.all()
    form = TagForm()

    context = {
        'tags': taglist,
        'form': form
    }

    return render(request, 'coredata/list/taglist.html', context)


#---------------------------------------------------------------------------------------------
#------------------------------------------Add Tags ---------------------------------------------
#---------------------------------------------------------------------------------------------


@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def AddTag(request):
    
    if request.method == 'POST':
        form = TagForm(request.POST)
        
        if form.is_valid():
            form.save()  
            
            return redirect('tags')  
        else:
            errors = form.errors
            return JsonResponse({'success': False, 'errors': errors})
    
    else:
        # Log the request method to help diagnose the issue
        print(f"Received a {request.method} request instead of a POST request.")
        return HttpResponseBadRequest("Invalid Request")
    

#---------------------------------------------------------------------------------------------
#------------------------------------------Edit Tags -----------------------------------------
#---------------------------------------------------------------------------------------------

@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def EditTag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)

    if request.method == 'POST':
        tag.name = request.POST.get('name')
        tag.save()
        return redirect('tags') 
        
    else:
        print(f"Received a {request.method} request instead of a POST request.")
        return HttpResponseBadRequest("Invalid Request")
    
    
#---------------------------------------------------------------------------------------------
#------------------------------------------Delete Tags ---------------------------------------
#---------------------------------------------------------------------------------------------
    

@login_required
@user_passes_test(is_superuser, login_url='access_denied')
def DeleteTag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    
    if request.method == 'POST':
        tag.name = request.POST.get('name')
        tag.delete()
        return redirect('tags')

    else:
        print(f"Received a {request.method} request instead of a POST request.")
        return HttpResponseBadRequest("Invalid Request")


#---------------------------------------------------------------------------------------------
#------------------------------------------News List ---------------------------------------
#---------------------------------------------------------------------------------------------


@login_required
def NewsList(request):
    
    newslist = News.objects.all()

    context = {
        'news': newslist,     
    }

    return render(request, 'modules/list/news.html', context)

#---------------------------------------------------------------------------------------------
#------------------------------------------News List ---------------------------------------
#---------------------------------------------------------------------------------------------

@login_required
def AddNews(request):

    tags = Tag.objects.all()
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news')
    else:
        form = NewsForm()
    return render(request, 'modules/add/newsadd.html', {'form': form, 'tags': tags})

@login_required
def EditNews(request, news_id):
    news_instance = get_object_or_404(News, id=news_id)
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news_instance)
        if form.is_valid():
            form.save()
            return redirect('news')
    else:
        form = NewsForm(instance=news_instance)

    return render(request, 'modules/edit/newsedit.html', {'form': form, 'tags': tags, 'news_instance': news_instance})

@login_required
def DeleteNews(request, id):
    news = get_object_or_404(News, id=id)
    
    if request.method == 'POST':
        news.delete()
        return redirect('news')

    else:
        print(f"Received a {request.method} request instead of a POST request.")
        return HttpResponseBadRequest("Invalid Request")
    


#---------------------------------------------------------------------------------------------
#------------------------------------------ Notice List --------------------------------------
#---------------------------------------------------------------------------------------------
def NoticeList(request):
    
    # Your view logic here
    noticelist = Notice.objects.all()
    form = NoticeForm()

    context = {
        'notice': noticelist,
        'form': form
    }

    return render(request, 'modules/list/notice.html', context)

#---------------------------------------------------------------------------------------------
#------------------------------------------ Add Notice --------------------------------------
#---------------------------------------------------------------------------------------------
@login_required
def AddNotice(request):

    form = NoticeForm()
    tags = Tag.objects.all()
    
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        
        if form.is_valid():
            form.save()  
            
            return redirect('notices')  
    else:
        form = NewsForm()
    return render(request, 'modules/add/notice.html', {'form': form, 'tags': tags})

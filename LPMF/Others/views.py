from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from Others.models import Articles, Services ,ToolsData , Category
from django.contrib.auth import login ,authenticate ,logout ,  update_session_auth_hash
from django.contrib.auth.models import User
from .forms import SignUpForm ,EditUserProfileForm , EditAdminProfileForm , CategoryDisplayForm
from django.contrib.auth.forms import UserChangeForm , AuthenticationForm , PasswordChangeForm , SetPasswordForm
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
import logging
# Create your views here.

def index(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return render(request, 'others/index.html', {'name': 'localisation' , 'ip':ip})


def about(request):
    about_article_obj = Articles.objects.get(article_heading_name="About us")
    return render(request, 'others/about.html', {'article_obj': about_article_obj})


def vision(request):
    vision_article_obj = Articles.objects.get(article_heading_name="Vision")
    return render(request, 'others/vision.html', {'article_obj': vision_article_obj})


def mission(request):
    mission_article_obj = Articles.objects.get(article_heading_name="Mission")
    return render(request, 'others/mission.html', {'article_obj': mission_article_obj})


def services(request):
    services = Services.objects.all()
    return render(request, 'others/services.html', {'services_obj': services})


def displayPrivacyPolicy(request):
    privacy_article_obj = Articles.objects.get(
        article_heading_name="Privacy Policy")
    return render(request, 'others/privacypolicy.html', {'article_obj': privacy_article_obj})


def termsandconditions(request):
    termsandcondition_article_obj = Articles.objects.get(
        article_heading_name="Terms & Conditions")
    return render(request, 'others/termsandcondition.html', {'article_obj': termsandcondition_article_obj})


# def display_tools(request):
#     tools_list = ToolsData.objects.all()
#     page = request.GET.get('page')  
#     paginator = Paginator(tools_list,1)
    
#     try:
#         post_list = paginator.page(page)
#     except PageNotAnInteger:
#         post_list = paginator.page(1)
#     except EmptyPage:
#         post_list = paginator.page(paginator.num_pages)
#     return render(request, 'others/tools.html',{'page': page, 'post_list':post_list})

def display_tools_with_category(request):
    if request.method == 'POST':
        catform  = CategoryDisplayForm(request.POST)
        if catform.is_valid():
            print('########################################')
            cat_name = catform.cleaned_data['category_name']
            print(cat_name)
            tools_list = ToolsData.objects.filter(tool_category = cat_name)
            print(tools_list)
            page = request.GET.get('page')  
            paginator = Paginator(tools_list,4)
            try:
                post_list = paginator.page(page)
            except PageNotAnInteger:
                post_list = paginator.page(1)
            except EmptyPage:
                post_list = paginator.page(paginator.num_pages)
            return render(request, 'others/tools.html',{'page': page, 'post_list':post_list , 'category': catform})
           
    else:
        tools_list = ToolsData.objects.all()
        cat_list =CategoryDisplayForm()
        page = request.GET.get('page')  
        paginator = Paginator(tools_list,4)
    
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        return render(request, 'others/tools.html',{'page': page, 'post_list':post_list, 'category':cat_list})


def display_resources(request):
    return render(request, 'others/resources.html')


def display_success_stories(request):
    a = Articles.objects.all()
    print("Printing Articles Values ")
    return render(request, 'others/success-stories.html', {'name': a})


def display_ap_success_stories(request):
    return render(request, 'others/ap-success-stories.html')


def disclaimer(request):
    a = Articles.objects.get(article_heading_name="Disclaimer")
    return render(request, 'others/disclaimer.html', {'dataobj': a})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print( "if form is valid")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/mission')
            else:
                return redirect('')
            
        else:
            form = AuthenticationForm()
            print( "else")
            return render(request, 'others/login.html', {'loginform': form})
    else:
        form = AuthenticationForm()
        return render(request, 'others/login.html', {'loginform': form})

def logout_user(request):
    print("inside logout function")
    logout(request)
    return redirect('/mission')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            messages.success(request,"Account Created Successfully ")
            return render(request, 'others/signup.html',{'form': form})
    else:
        form = SignUpForm()
    return render(request, 'others/signup.html', {'form': form})

def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm = PasswordChangeForm(user=request.user , data= request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                messages.success(request,"Password Changed Successfully")
                return HttpResponseRedirect('/profile/')
        else:
            fm = PasswordChangeForm(user=request.user)
            return render(request,'others/changepass.html',{'fm':fm})
        return render(request,'others/changepass.html',{'name': request.user.username,'fm':fm})
    else:
        return HttpResponseRedirect('/login_user/')

def profile(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            if request.user.is_superuser == True:             
                fm = EditAdminProfileForm(request.POST , instance=request.user)
                users = User.objects.all()
                if fm.is_valid():
                    messages.success(request,"Profile Updated Successfully")
                    fm.save()
                    return HttpResponseRedirect('/profile')
            else:
                users = None
                fm = EditUserProfileForm(request.POST , instance = request.user)
                if fm.is_valid():
                    messages.success(request,"Profile Updated Successfully")
                    fm.save()
                    return render(request , 'others/profile.html',{'name':request.user.username,'fm':fm,'users':users})
        else:
            if request.user.is_superuser == True:        
                fm = EditAdminProfileForm(instance=request.user)
                users = User.objects.all()
                return render(request,'others/profile.html',{'name': request.user.username,'fm':fm, 'users':users})  
            else:
                fm = EditUserProfileForm(instance = request.user)
                return render(request,'others/profile.html',{'name': request.user.username,'fm':fm})  
    else:
        return HttpResponseRedirect('/login_user')

def userdetail(request,id):
    if request.user.is_authenticated:
        pi = User.objects.get(pk=id)
        fm = EditAdminProfileForm(instance=pi)
        return render(request,'others/userdetail.html',{'fm':fm})
    else:
        return HttpResponseRedirect('/login_user')
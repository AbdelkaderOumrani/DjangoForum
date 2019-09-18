from django.shortcuts import render,get_object_or_404, get_list_or_404
from django.contrib import messages, auth
from django.contrib.auth import logout as django_logout
from django.contrib.auth import password_validation as validators
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from .validators import UsernameValidator, NameValidator, EmailValidator
from .models import Profile
from posts.models import Comment,Post
from django.db.models import Q
import os
from django.conf import settings
from django.core.exceptions import ValidationError
#------------------------------
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage



def register(request):
    if request.user.is_authenticated:
        return redirect('recent_posts')
    elif request.POST:
        isValid = True
        first_name = request.POST['first_name']
        if not NameValidator(first_name):
            messages.error(request,'Invalid First Name')
            isValid = False
        last_name = request.POST['last_name']
        if not NameValidator(last_name):
            messages.error(request,'Invalid Last Name')
            isValid = False
        username = request.POST['username']
        if not UsernameValidator(username):
            messages.error(request,'invalid username pattern')
            isValid=False
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username Already Exists')
            isValid = False
        email = request.POST['email']
        if not EmailValidator(email):
            messages.error(request,'Invalid Email')
            isValid = False
        elif User.objects.filter(email=email).exists():
            messages.error(request,'Email Already Exists')
            isValid = False
        password = request.POST['password']
        password2 = request.POST['password2']
        if not password==password2:
            messages(request,'Passwords Do not match')
            isValid = False
        else:
            try:
                validators.validate_password(password)
            except ValidationError as err:
                for message in err.messages:
                    messages.error(request,message)
                    isValid = False
        
        if isValid:
            user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                                    username=username, 
                                                    email=email, 
                                                    password=password,
                                                    is_active=False)
            current_site = get_current_site(request)
            mail_subject = 'Activate your EsiForum account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
                })
            to_email = email
            email = EmailMessage(
            mail_subject, message, to=[to_email])
            email.send()
            messages.warning(request,'Please confirm your email address to complete the registration')
            return redirect('login')  
        else:
            return redirect('register')                         

    else:
        return render(request, 'accounts/register.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Account Activated Successfully')
        return redirect('login')
    else:
        return HttpResponse('invalid token')


def login(request):
    if request.user.is_authenticated:
        return redirect('categories')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('recent_posts')
            else:
                messages.error(request, 'your account is not active')
                return redirect('login')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    username = request.user.username
    django_logout(request)
    return HttpResponseRedirect('login')


def edit_profile(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/edit_profile.html')


def show_profile(request,user_id):
    if request.user.is_authenticated:
        found_user = get_object_or_404(User, pk=user_id)
        user_nb_posts = Post.objects.filter(author=found_user).count()
        user_nb_comments = Comment.objects.filter(author=found_user).count()
        user_posts = Post.objects.filter(author=found_user)
        context = {
            'user_posts':user_posts,
            'found_user':found_user,
            'user_nb_posts' : user_nb_posts,
            'user_nb_comments' : user_nb_comments
        }

        return render(request, 'accounts/show_profile.html',context)
    else:
        return redirect('login')


def change_username(request):
    if request.POST:
        username = request.POST['inputChangeUsername']
        if UsernameValidator(username):
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            else:
                user = User.objects.get(id=request.user.id)
                user.username = username
                user.save()
                messages.success(request, 'Username changed successfully')
        else:
            messages.error(request, 'Username is not allowed')
    return render(request, 'edit_profile')


def change_fullname(request):
    if request.POST:
        lastName = request.POST['inputChangeLastName']
        firstName = request.POST['inputChangeFirstName']
        if NameValidator(lastName) and NameValidator(firstName):
            user = User.objects.get(id=request.user.id)
            user.first_name = firstName
            user.last_name = lastName
            user.save()
            messages.success(request, 'Your name changed successfully')
        else:
            messages.error(request, 'Non allowed name pattern')
    return redirect('edit_profile')


def change_email(request):
    if request.POST:
        email = request.POST['inputChangeEmail']
        if EmailValidator(email):
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.get(id=request.user.id)
                user.email = email
                user.save()
                messages.success(request, 'Email changed successfully')
        else:
            messages.error('Non valid Email')
    return redirect('edit_profile')


def change_bio(request):
    if request.POST:
        bio = request.POST['inputChangeBio']
        if len(bio) > 200:
            messages.error(request, '200 characters Maximum')
        else:
            profile = Profile.objects.get(user=request.user)
            profile.bio = bio
            profile.save()
            messages.success(request, 'Your Bio changed Successfully')
    return redirect('edit_profile')


def change_avatar(request):
    if request.POST:
        avatar = request.FILES['inputChangeAvatar']
        if avatar.size > 200000:
            messages.error(request, 'max file size is 200 Kb')
        else:
            profile = Profile.objects.get(user = request.user)
            oldp = profile.avatar
            profile.avatar = avatar
            profile.save()
            if not oldp.name.endswith('/empty.png'):
                os.remove(os.path.join(settings.MEDIA_ROOT, oldp))            
            messages.success(request, 'Profile Picture Changed successfully')
    return redirect('edit_profile')

def change_password(request):
    if request.POST:
        u = User.objects.get(id = request.user.id)
        oldpass = request.POST['inputOldPassword']
        newpass = request.POST['inputNewPassword']
        confirmpass = request.POST['inputConfirmPassword']
        if u.check_password(oldpass):
            if newpass == confirmpass:
                try:
                    validators.validate_password(newpass)
                except ValidationError as err:
                    for message in err.messages:
                        messages.error(request,message)
                else:
                    u.set_password(newpass)
                    u.save()
                    messages.success(request,'Password Changed Successfully, Login with your new password')
                    django_logout(request)
                    return redirect('login')
                    

            else:
                messages.error(request,'Password and Confirmation do not match')
        else:
            messages.error(request,'Old Password not correct')

    return redirect ('edit_profile')


def deactivate_account(request):
    if request.POST:
        u = User.objects.get(id = request.user.id)
        u.is_active = False
        u.save()
        messages.success(request,'Your Account deactivated successfully')
        django_logout(request)
    return redirect('login')
        
def users_list(request):
    if request.user.is_authenticated:
        users = User.objects.all()    
        if request.POST:
            find = request.POST['search_user']
            return redirect(find_users,search_val=find)
        context = {
            'users':users
        }
        return render (request,'accounts/users_list.html',context)
    else:
        return redirect(login)

def find_users(request,search_val):
    if request.user.is_authenticated:
        users = User.objects.filter(Q(username__icontains=search_val)|
                                    Q(first_name__icontains=search_val)|
                                    Q(last_name__icontains=search_val))
        context = {
                'users':users,
                'search_val':search_val
                }
        return render(request,'accounts/find_users.html',context)
    else:
        return redirect(login)
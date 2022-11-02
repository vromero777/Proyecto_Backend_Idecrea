from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from weblogin import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username not available")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email already in use")
            return redirect('signup')

        if len(username)>10:
            messages.error(request, "Username most be under 10 characters")
            return redirect('signup')


        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')



        if not username.isalnum():
            messages.error(request, "Username most be alpha-numeric")
            return redirect('signup')


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account has been successfully created.")


        #WELCOME EMAIL

        subject = "Welcome to Wolow"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcomne to Wolow \n Thank you for visiting our webapp \n  We have also sent you a confirmation email, please confirm your email address to activate your account "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')


    return render(request, "authentication/signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname' : fname})
        else:
            messages.error(request, "Username or Password do not match")
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')
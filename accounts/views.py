from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Account
from .models import Teacher
from django.http import HttpResponseNotFound
from forms import views
from django.contrib.auth.views import password_reset
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, 'accounts/home.html')
def thome(request):
    return render(request, 'accounts/thome.html')

def signup(request):
    if request.method == 'POST':
        # Submitted info
        if request.POST['id'] and request.POST['name'] and request.POST['password1'] and request.POST['password2'] and request.POST['email'] and request.POST['department']:
            if request.POST['password1'] == request.POST['password2']:
                if len(request.POST['password1']) <= 5:
                    return render(request, 'accounts/home.html', {'error': 'Password length must be greater than 5'})
                
                try:
                    user = User.objects.get(username=request.POST['id'])
                    return render(request, 'accounts/home.html', {'error': 'ID has already been taken'})
                except User.DoesNotExist:
                    user = User.objects.create_user(request.POST['id'], password=request.POST['password1'], email=request.POST['email'])
                    #auth.login(request,user)
                    
                    account = Account()
                    account.Id = request.POST['id']
                    account.Name = request.POST['name']
                    account.Email = request.POST['email']
                    #account.Session = request.POST['session']
                    account.Department = request.POST['department']
                    account.save()
                    
                    #return redirect('/accounts/dashboard/' + str(account.id))
                    send_mail('Registration on Course Registration Management','Your registration form has been received. Please wait for verification.','hollowman697@gmail.com',[request.POST['email']],fail_silently=False,)
                    return render(request, 'accounts/home.html', {'error': 'Please wait for verification. An email has been sent to your e-mail address.'})
            else:
                return render(request, 'accounts/home.html', {'error': 'Passwords must match'})
        else:
            return render(request, 'accounts/home.html', {'error': 'No fields should be left empty'})
    else:
        # Will enter info
        return render(request, 'accounts/home.html')
    
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            pid = -1
            accounts = Account.objects
            for a in accounts.all():
                try:
                    if a.Id == int(request.POST['username']):
                        pid = a.id
                        if a.Verified == False:
                            pid = -2
                        break
                except ValueError:
                    return render(request, 'accounts/home.html', {'error':'Username or password is incorrect'})

            if pid >= 0:
                auth.login(request, user)
            elif pid == -2:
                return render(request, 'accounts/home.html', {'error':'Your account is not verified. Wait for verification.'})
            else:
                return render(request, 'accounts/home.html', {'error':'Username or password is incorrect'})
                    
            return redirect('/accounts/dashboard/' + str(pid))
        else:
            return render(request, 'accounts/home.html', {'error':'Username or password is incorrect'})
    else:   
        return render(request, 'accounts/home.html')

def tsignup(request):
    if request.method == 'POST':
        # Submitted info
        if request.POST['name'] and request.POST['password1'] and request.POST['password2'] and request.POST['email'] and request.POST['department'] and request.POST['designation']:
            if request.POST['password1'] == request.POST['password2']:
                if len(request.POST['password1']) <= 5:
                    return render(request, 'accounts/thome.html', {'error': 'Password length must be greater than 5'})
                
                try:
                    user = User.objects.get(username=request.POST['email'])
                    return render(request, 'accounts/thome.html', {'error': 'E-mail has already been taken'})
                except User.DoesNotExist:
                    user = User.objects.create_user(request.POST['email'], password=request.POST['password1'], email=request.POST['email'])
                    #auth.login(request,user)
                    
                    account = Teacher()
                    account.Name = request.POST['name']
                    account.Email = request.POST['email']
                    account.Department = request.POST['department']
                    account.Designation = request.POST['designation']
                    account.save()
                    
                    #return redirect('/accounts/tdashboard/' + str(account.id))
                    send_mail('Registration on Course Registration Management','Your registration form has been received. Please wait for verification.','hollowman697@gmail.com',[request.POST['email']],fail_silently=False,)
                    return render(request, 'accounts/thome.html', {'error': 'Please wait for verification. An email has been sent to your e-mail address.'})
            else:
                return render(request, 'accounts/thome.html', {'error': 'Passwords must match'})
        else:
            return render(request, 'accounts/thome.html', {'error': 'No fields should be left empty'})
    else:
        # Will enter info
        return render(request, 'accounts/thome.html')
    
def tlogin(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['email'],password=request.POST['password'])
        if user is not None:
            pid = -1
            accounts = Teacher.objects
            for a in accounts.all():
                if a.Email == request.POST['email']:
                    pid = a.id
                    if a.Verified == False:
                        pid = -2
                    break
            
            if pid >= 0:
                auth.login(request, user)
            elif pid == -2:
                return render(request, 'accounts/thome.html', {'error':'Your account is not verified. Wait for verification.'})
            else:
                return render(request, 'accounts/thome.html', {'error':'Username or password is incorrect'})
     
            return redirect('/accounts/tdashboard/' + str(pid))
        else:
            return render(request, 'accounts/thome.html', {'error':'Username or password is incorrect'})
    else:   
        return render(request, 'accounts/thome.html')

@login_required(login_url="home") 
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

@login_required(login_url="thome") 
def tlogout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('thome')

@login_required(login_url="home")    
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required(login_url="home") 
def dashboard(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    
    cur_user = request.user
    if int(cur_user.username) != account.Id:
        return HttpResponseNotFound("<center><b><font size=40>403 FORBIDDEN!</font></b></center>")
    
    return render(request, 'accounts/dashboard.html', {'account':account})

@login_required(login_url="thome") 
def tdashboard(request, teacher_id):
    taccount = get_object_or_404(Teacher, pk=teacher_id)
    cur_user = request.user
    if cur_user.username != taccount.Email:
        return HttpResponseNotFound("<center><b><font size=40>403 FORBIDDEN!</font></b></center>")

    if request.method=='POST':
        tot = "/forms/formlists/"
        y = request.POST['year']
        sem = request.POST['semester']
        if(sem == "Odd"):
            tot += str(y) + "-1"
        else:
            tot += str(y) + "-2"

        tot += "&id~" + str(teacher_id)
        return redirect(tot)

    return render(request, 'accounts/tdashboard.html', {'tid':teacher_id})
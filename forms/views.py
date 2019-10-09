from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Form
from .models import Counter
from django.utils import timezone
from accounts.models import Account
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.db import connection
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
import base64
import matplotlib
matplotlib.use("Agg")


@login_required(login_url="/accounts/home") 
def regform(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    try:
        if int(request.user.username) != account.Id:
            return HttpResponseNotFound("<center><b><font size=40>403 FORBIDDEN!</font></b></center>")
    except ValueError:
        return HttpResponseNotFound("<center><b><font size=40>403 FORBIDDEN!</font></b></center>")

    if request.method=='POST':
        if request.POST['roll'] and request.POST['regno'] and request.POST['session'] and request.POST['name'] and request.POST['semester'] and request.POST['totalcredit']:

            if int(request.user.username) != int(request.POST['roll']):
                return render(request, 'forms/regform.html', {'error': 'Roll mismatched!', 'account':account})  

            field1 = '%' + request.POST['semester'][0]
            field2 = field1
            if request.POST['semester'].find('1', 1) != -1 or request.POST['semester'].find('odd') != -1:
                field1 = field1 + '%1%'
                field2 = field2 + '%odd%'
            else:
                field1 = field1 + '%2%'
                field2 = field2 + '%even%' 

            qry = 'DELETE FROM forms_Form WHERE semester ILIKE %(num)s OR semester ILIKE %(text)s AND roll=%(roll)s'
            params = {'num':field1, 'text':field2, 'roll':request.user.username}
            #forms = Form.objects.raw(qry, params)
            with connection.cursor() as cursor:
                cursor.execute(qry, params)

            form = Form()
            form.roll = request.POST['roll']
            form.regno = request.POST['regno']
            form.session = request.POST['session']
            form.name = request.POST['name']
            form.semester = request.POST['semester']
            form.totalcredit = request.POST['totalcredit']
            form.date = timezone.datetime.now()
            form.backlog = request.POST['backlog']
            
            courseNo = ""
            courseTitle = ""
            credit = ""
            
            for i in range(11):
                if i == 0:
                    continue
                k1 = "courseno" + str(i)
                k2 = "title" + str(i)
                k3 = "credit" + str(i)
                
                if request.POST[k1] and request.POST[k2] and request.POST[k3]:
                    if len(courseNo) != 0:
                        courseNo += ","
                        courseTitle += ","
                        credit += ","
                        
                    courseNo += request.POST[k1]
                    courseTitle += request.POST[k2]
                    credit += request.POST[k3]
                    
            form.courseno = courseNo
            form.title = courseTitle
            form.credit = credit
            
            form.save()
            
            return redirect('/accounts/dashboard/' + str(account_id))
            
        else:
            return render(request, 'forms/regform.html', {'error': 'Fill The Compulsory Fields', 'account':account})    
        
    return render(request, 'forms/regform.html', {'account':account})

@login_required(login_url="thome") 
def formlists(request, ys_id):
    #forms = Form.objects.order_by('roll')
    cur_user = request.user
    if cur_user.username.find('@') == -1:
        return HttpResponseNotFound("<center><b><font size=40>403 FORBIDDEN!</font></b></center>")

    field1 = '%' + ys_id[0]
    field2 = field1
    if ys_id[2] == '1':
        field1 = field1 + '%1%'
        field2 = field2 + '%odd%'
    else:
        field1 = field1 + '%2%'
        field2 = field2 + '%even%' 

    qry = 'SELECT * FROM forms_Form WHERE semester ILIKE %(num)s OR semester ILIKE %(text)s ORDER BY roll'
    params = {'num':field1, 'text':field2}
    forms = Form.objects.raw(qry, params)

    temp = ys_id.split('~')
    return render(request, 'forms/formlists.html', {'forms':forms, 'tid':int(temp[1]), 'ys_id':ys_id})

@login_required(login_url="thome") 
def detail(request, form_id):
    cur_user = request.user
    if cur_user.username.find('@') == -1:
        return HttpResponseNotFound("<center><b><font size=40>403 FORBIDDEN!</font></b></center>")

    form = get_object_or_404(Form, pk=form_id)
    
    s = form.courseno
    courses = s.split(',')

    s = form.title
    titles = s.split(',')

    s = form.credit
    credits = s.split(',')

    info = zip(courses, titles, credits)

    s = form.backlog + " "
    return render(request, 'forms/detail.html', {'form':form, 'info':info, 'backlog':s})

@login_required(login_url="thome") 
def plot(request, ys_id):

    field1 = '%' + ys_id[0]
    field2 = field1
    if ys_id[2] == '1':
        field1 = field1 + '%1%'
        field2 = field2 + '%odd%'
    else:
        field1 = field1 + '%2%'
        field2 = field2 + '%even%' 

    qry = 'SELECT id FROM forms_Form WHERE semester ILIKE %(num)s OR semester ILIKE %(text)s'
    params = {'num':field1, 'text':field2}
    submitted = Form.objects.raw(qry, params)
    submitted = len(list(submitted))
    total = 0

    if ys_id[0] == '1':
        if ys_id[1] == '1':
            total = Counter.objects.first().oneOdd
        else:
            total = Counter.objects.first().oneEven
    elif ys_id[0] == '2':
        if ys_id[1] == '1':
            total = Counter.objects.first().twoOdd
        else:
            total = Counter.objects.first().twoEven
    elif ys_id[0] == '3':
        if ys_id[1] == '1':
            total = Counter.objects.first().threeOdd
        else:
            total = Counter.objects.first().threeEven
    else:
        if ys_id[1] == '1':
            total = Counter.objects.first().fourOdd
        else:
            total = Counter.objects.first().fourEven
            
    # defining labels 
    activities = ['Pending', 'Submitted']
    
    # portion covered by each label 
    slices = [total-submitted, submitted] 
    
    # color for each label 
    colors = ['r', 'g'] 
    
    # plotting the pie chart 
    plt.pie(slices, labels = activities, colors=colors,  
            startangle=90, shadow = True, explode = (0.1, 0), 
            radius = 1.2, autopct = '%1.1f%%') 
    
    # plotting legend 
    plt.legend() 
    
    # showing the plot 
    #plt.show() 

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    plt.close()

    # x-coordinates of left sides of bars  
    left = [1, 2] 
    
    # heights of bars 
    height = [submitted, total-submitted] 
    
    # labels for bars 
    tick_label = ['Submitted', 'Pending'] 
    
    # plotting a bar chart 
    plt.bar(left, height, tick_label = tick_label, 
        width = 0.5, color = ['green', 'red']) 
    
    # naming the x-axis 
    plt.xlabel('Submission Status') 
    # naming the y-axis 
    plt.ylabel('No of Students') 
    # plot title 
    plt.title('Bar Chart') 

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image2_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    plt.close()

    return render(request, 'forms/plot.html', {'image_base64':image_base64, 'image2_base64':image2_base64})
from django.shortcuts import render, HttpResponse, redirect
from rail_ticket_app.models import Train
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def home(request):
       print("Method is",request.method)
       if request.method =="GET":
            return render(request,'index.html')
       else:
              #return HttpResponse("insert data into DB")
            n=request.POST['name']
            print("Name is",n)
       return HttpResponse("Values fetched successfully")
  
def search(request):
     context={}
     fromStation=request.GET['fromStn']
     toStation=request.GET['toStn']
     j=request.GET['journeyDate']
     if fromStation=="" or toStation=="" or j=="":
            context['Errormsg']="Field cannot be empty"
            return render(request,'index.html',context)
     q1=Q(source=fromStation)
     q2=Q(destination=toStation)
     t=Train.objects.filter(q1 & q2)
     
     print(t)
     context={}
     context['fromStn']=fromStation
     context['toStn']=toStation
     context['trains']=t
     context['journeyDate']=j
     context['selectedClass']=''
     return render(request,'show_train.html',context)
     
def check_PNR(request):
     return render(request,'pnr.html')

def chart(request):
     return render(request,'reservation_chart.html')

def ticket_details(request):
     return HttpResponse("ok")

def book_ticket(request):
     if request.user.is_authenticated:
          context={}
          seletedClass=request.POST['seletedClass']
          trainContext=request.POST['trainContext']
          arrivalTime=request.POST['arrivalTime']
          sourceStn=request.POST['sourceStn']
          destStn=request.POST['destStn']
          jDate=request.POST['jDate']
          tFare=request.POST['tFare']
          context['seletedClass']=seletedClass
          context['trainContext']=trainContext
          context['arrivalTime']=arrivalTime
          context['sourceStn']=sourceStn
          context['destStn']=destStn
          context['jDate']=jDate
          context['tFare']=tFare
          return render(request,'book_ticket.html',context)
     else:          
          return redirect('/login')
               
def confirm_ticket(request):
     payment =request.POST['payment']
     context={}
     context['payment']=payment
     if request.method== 'POST':   
          status  = request.POST.get('paymentStatus')
          if status == 'success':
            # Redirect to the print_ticket
            return print_ticket(request,context)
          else:
            # show error pop and go back to home page
            return render(request, 'payment.html',context)  

def print_ticket(request,context):
     return render(request,'print_ticket.html',context)

def login(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        if uname=="" or upass=="":
            context['Errormsg']="Field cannot be empty"
            return render(request,'login.html',context)
        
        else:
            u=authenticate(username=uname,password=upass) # is work as select qurey...when user name password not match is written none 
            if u is not None :
                login(request)
                return redirect('/home')
            else:
                context['Errormsg']="Invalid username and password"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')
   
def register(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        if uname=="" or upass=="" or ucpass=="":
            context['Errormsg']="Field cannot be empty"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context['Errormsg']="Passwoard did not match"
            return render(request,'register.html',context)
                       
        else:
            try:
                u=User.objects.create(username=uname,password=upass,email=uname )
                u.set_password(upass)
                u.save()
                context['Success']="User added successfully"
                return redirect('/home')
            except Exception:
                context['Errormsg']="Username already exits"
                return render(request,'register.html',context)
                             
    else:
        return render(request,'register.html')
       
def logout(request):
    logout(request)
    return redirect("/home")
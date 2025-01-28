from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib import messages
import random



def index(request):
    return render(request,'index.html')







# Create your views here.
def userregister(request):
    if request.method == 'POST':
        name1=request.POST.get('user_name')
        password1=request.POST.get('pass_word')
        name = request.POST.get('name') 
        e_mail1=request.POST.get('e_mail')
        phone1=request.POST.get('phone')
        customuser_obj=CustomUser.objects.create_user(
                                            first_name=name,
                                            username=name1,
                                            password=password1,
                                            email=e_mail1,
                                            phone_number=phone1)
        customuser_obj.save()
    return render(request,"user_register.html") 
def user_login(request):
    if request.method == 'POST':
        username1=request.POST.get('user_name')
        password1=request.POST.get('pass_word')
        user=authenticate(username=username1,password=password1)
        admin_user=authenticate(request,username=username1,password=password1)
        if admin_user is not None and admin_user.is_staff:
            login(request,admin_user)
            return redirect('adminhome')
        elif user is not None:
            login(request,user)
            return redirect('userhome')
        else:
            context={'data':'credentials invalid'}
            return render(request,'user_login.html',context)

    else:
        return render(request,'user_login.html')
def userhome(request):
    data=book.objects.all()
    return render(request,'userhome.html',{'datas':data})
    
def userprofile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"userprofile.html",{'data':user})
def userupdate(request):
    user=CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
                user.first_name = request.POST.get('name') 
                user.email=request.POST.get('e_mail')
                user.phone_number=request.POST.get('phone')
                user.save()
                return redirect('userprofile')
    else:
        return render(request,"userprofile_update.html",{'data':user})







def adminhome(request):
     return render(request,"admin_home.html")
def userdetails(request):
     data=CustomUser.objects.filter(is_staff=False)
     return render(request,"userdetails.html",{'datas':data})
def categorydeatails(request):
     data=category.objects.all()
     return render(request,"category_details.html",{'datas':data})
def categoryadd(request):
    if request.method == 'POST':
        category_name1=request.POST.get('category')
        category_obj=category()
        category_obj.category_name=category_name1
        category_obj.save()
        return redirect('categorydetail')
    return render(request,"category_add.html")
def categorydelete(request,id):
     data=category.objects.get(id=id)
     data.delete()
     return redirect('categorydetail')



def bookdetails(request):
     data=book.objects.all()
     return render(request,"book_details.html",{'datas':data})


def addbook(request):
     data = category.objects.all()
     if request.method == 'POST':
          name1=request.POST.get('book_name')
          auther1=request.POST.get('book_auther')
          price1=request.POST.get('book_price')
          category1=category.objects.get(id=request.POST.get('book_category'))
          quantity1=request.POST.get('book_quantity')
          publisher1=request.POST.get('book_publisher')
          published_date1=request.POST.get('publisheddate')
          book_obj=book.objects.create(name=name1,auther=auther1,price=price1,category=category1,quantity=quantity1,publisher=publisher1,published_date=published_date1)
          book_obj.save()
          return redirect('bookdetails')
     else:
          return render(request,"book_add.html",{'datas':data})   
def bookupdate(request,id):
     data=book.objects.get(id=id)
     data1=category.objects.all()
     if request.method == 'POST':
         data.name=request.POST.get('book_name')
         data.auther=request.POST.get('book_auther')
         data.price=request.POST.get('book_price')
         category_id=request.POST.get('book_category')
         if category_id:
           data.category=category.objects.get(id=category_id)
         data.quantity=request.POST.get('book_quantity')
         data.publisher=request.POST.get('book_publisher')
         data.published_date=request.POST.get('publisheddate')
         data.save()
         return redirect('bookdetails')
     return render(request,"book_update.html",{'datas':data,'datas1':data1})
def bookdelete(request,id):
     data=book.objects.get(id=id)
     data.delete()
     return redirect('bookdetails')








def send_otp(email):
    otp=random.randint(100000,999999)
    send_mail('your otp code ',f'your otp code is {otp}','sajitharahman1997@gmail.com',[email],fail_silently=False,)
    return otp

def Password_reset_request(request):
    if request.method=='POST':
        email=request.POST['email']
        try:
            user=CustomUser.objects.get(email=email)
            otp=send_otp(email)
            print(user)
            context={
                'email':email,
                'otp':otp
            }
            return render(request,'verify_otp.html',context)
        except CustomUser.DoesNotExist:
            messages.error(request,'email address not found')
    else:
        return render(request,'password_reset.html')
    return render(request,'password_reset.html')

def Verify_otp(request):
    if request.method=='POST':
        email=request.POST.get('email')
        otpold=request.POST.get('otp')
        otp=request.POST.get('otp1')
        if otpold==otp:
            context={'otp':otp,
                     'email':email}
            return render(request,'new_password.html')
        else:
            messages.error(request,'Invalid otp')
    return render(request,'verify_otp.html')
def Set_new_password(request):
    if request.method=='POST':
        email=request.POST.get('email')
        new_password=request.POST.get('password1')
        confirm_password=request.POST.get('password2')
        if new_password==confirm_password:
            try:
                data=CustomUser.objects.get(email=email)
                data.set_password(new_password)
                data.save()
                messages.success(request,'password has been reset successfully')
                return redirect('login')
            except data.DoesNotExist:
                messages.error(request,'password doesnot match')
        return render(request,'new_password.html',{'email':email})
    return render(request,'new_password.html',{'email':email})


# def temperory(request):
#     return render(request,"temp.html")


# def users_bookview(request):
#     data=book.objects.all()
#     return render(request,"book_details.html",{'datas':data})
  
        

    
    

    


    


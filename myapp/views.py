from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib import messages
import random
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger



def index(request):
    data=book.objects.all()
    return render(request,'index.html',{'datas':data})







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
        return redirect('index')
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
def catagorypage(request,catagory):
    catagory_obj=category.objects.get(category_name=catagory)
    data=book.objects.filter(category=catagory_obj)
    return render(request,"catagorypage.html",{'datas':data})
def book_accept(request,id):
    data=book.objects.get(id=id)
    user_det = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if(data.quantity>=quantity):
            total_amount = data.price * quantity
            booking_obj=booking()
            booking_obj.user_id=user_det
            booking_obj.book_id=data
            booking_obj.quantity=quantity
            booking_obj.total_amount=total_amount
            booking_obj.save()
            return redirect('book_accept',id=data.id)
        else:
            return render(request,'book_accept.html',{'datas':data,'error':"out of stock"})

        

    return render(request,'book_accept.html',{'datas':data})

def booking_view(request):
    data1=CustomUser.objects.get(id=request.user.id)
    data2=booking.objects.filter(user_id=data1.id)
    items_per_page=2
    paginator=Paginator(data2,items_per_page)
    page=request.GET.get('page',1)

    try:
        data2=paginator.page(page)
    except PageNotAnInteger:
        data2=paginator.page(1)
    except EmptyPage:
        data2=paginator.page(paginator.num_pages) 
    context={
        'datas':data2,
    }
    return render(request,"booking_view.html",context)


import stripe
from django.conf import settings 

stripe.api_key = settings.STRIPE_SECRET_KEY

def stripe_payment(request,id):
    try:
        data=booking.objects.get(id=id)
        total_amount = data.total_amount
            

        intent = stripe.PaymentIntent.create(
            amount=int(total_amount*100),
            currency="usd",
            metadata={"data":data,"user_id":request.user.id},

        )
        context = {
            'client_secret': intent.client_secret,
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
            'total_amount':total_amount,
            'data':data,
        }
        return render(request,'stripe_payments.html',context)
        
    except booking.DoesNotExist:
        return redirect(userhome)
    
def payment_status(request,id):
    data=booking.objects.get(id=id)
    data.payment='Completed'
    data.save()
    return redirect(booking_view)












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
def booking_list(request):
    data=booking.objects.all()
    return render(request,"booking_list.html",{'datas':data})
def statusing(request,id):
     data=booking.objects.get(id=id)
     if request.method == "POST":
         status1=request.POST.get('status')
         if status1=='Accept':
            data.status="Accept"
         elif status1=='Reject':
             data.status="Reject"
     data.save()
     return redirect('booking_list')
def bookdetails(request):
     data=book.objects.all()
     return render(request,"book_details.html",{'datas':data})

def bookdelete(request,id):
    data=book.objects.get(id=id)
    data.delete()
    redirect('bookdetails')
def bookpage(request,id):
    data=book.objects.get(id=id)
    return render(request,"bookpage.html",{'datas':data})    
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
          image1=request.FILES['imagee']
          book_obj=book.objects.create(name=name1,auther=auther1,price=price1,category=category1,quantity=quantity1,publisher=publisher1,published_date=published_date1,image=image1)
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



def temperory(request):
    return render(request,"temp.html")

def temp1(request):
    return render(request,"temp1.html")
def temp2(request):
    return render(request,"temp2.html")











# def users_bookview(request):
#     data=book.objects.all()
#     return render(request,"book_details.html",{'datas':data})
  
        

    
    

    


    


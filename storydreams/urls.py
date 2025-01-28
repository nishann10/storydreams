"""
URL configuration for storydreams project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('register',views.userregister,name='register'),
    path('login',views.user_login,name='login'),



    path('userhome',views.userhome,name='userhome'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('update',views.userupdate,name='update'),


    path('adminhome',views.adminhome,name='adminhome'),
    path('userdetail',views.userdetails,name='userdetail'),
    path('categorydetail',views.categorydeatails,name='categorydetail'),
    path('categoryadd',views.categoryadd,name='categoryadd'),
    path('categorydlt/<int:id>', views.categorydelete,name='categorydlt'),



    path('bookdetails',views.bookdetails,name='bookdetails'),
    path('bookadd',views.addbook,name='bookadd'),
    path('bookupdate/<int:id>',views.bookupdate,name='bookupdate'),
    path('bookdelete/<int:id>',views.bookdelete,name='bookdelete'),



    path('password_reset',views.Password_reset_request,name='password_reset'),
    path('verify_otp',views.Verify_otp,name='verify_otp'),
    path('set_new_password',views.Set_new_password,name='set_new_password'),


]
if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    
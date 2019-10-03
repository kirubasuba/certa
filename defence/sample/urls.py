from django.urls import path
from django.conf.urls import url, include
from . import views
from . import dbview

urlpatterns=[
    path('',views.viewclass.index,name='index'),
    path('login',views.viewclass.login,name='login'),
    path('logout',views.viewclass.logout,name='logout'),
    path('adminmenulist1',views.viewclass.adminmenulist1,name='adminmenulist1'),
    path('login_new',views.viewclass.login_new,name='login_new'),
    path('login_1',views.viewclass.login_1,name='login_1'),
    path('add',views.viewclass.index,name='index'),
    path('loggedin',views.viewclass.loggedin,name='loggedin'),
    path('sign_up',views.viewclass.sign_up,name='sign_up'),
    path('get',views.viewclass.get,name='get'),
    path('NewUser',views.viewclass.NewUser,name='NewUser'),
    path('newuserregistration',views.viewclass.newuserreg,name='newuserreg'),
    path('userdetails', views.viewclass.userDetails),
    path('display',views.viewclass.userDetails),
    path('View',views.viewclass.viewfirm),
    path('New',views.viewclass.NewUser)

]
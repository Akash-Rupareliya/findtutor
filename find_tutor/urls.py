from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    
    #path('login/',auth_views.LoginView.as_view(template_name='auth/login.html'),name="login_page"),
    path('admintemplate/',views.adminlogin,name='adminlogin'),
    path('admintemplate/home',views.admin_index,name="admin_index"),
    path('admintemplate/addsubject',views.addsubject,name='addsubject'),
    path('admintemplate/addcategory',views.addcategory,name="addcategory"),
    path('admintemplate/addsubcategory',views.addsubcategory,name="addsubcategory"),
    path('admintemplate/addcity',views.addcity,name='addcity'),
    path('admintemplate/addstate',views.addstate,name='addstate'),

    #path('admin_login',views.admin_login,name='admin_login'),
    path('admintemplate/admin_logout',views.admin_logout,name='admin_logout'),
    path('admintemplate/admin_login',views.admin_login,name='admin_login'),
    
    
    path('admintemplate/viewregisteredusers',views.viewregisteredusers,name='viewregisteredusers'),
    path('admintemplate/viewstudents',views.viewstudents,name='viewstudents'),
    path('admintemplate/viewtutor',views.viewtutor,name='viewtutor'),
    path('admintemplate/viewstate',views.viewstate,name='viewstate'),
    path('admintemplate/viewcategory',views.viewcategory,name='viewcategory'),
    
    path('upload_csv',views.upload_csv,name='upload_csv'),
    path('upload_csv_category',views.upload_csv_category,name='upload_csv_category'),
    
    path('delete_user/<int:id>',views.delete_user,name='delete_user'),
    path('delete_stud/<int:id>',views.delete_stud,name='delete_stud'),
    path('delete_tutor/<int:id>',views.delete_tutor,name='delete_tutor'),

    path('',views.user_index,name='user_index'),
    path('about/',views.about_page,name="about"),
    path('contact/',views.contact_page,name="contact"),
    path('registration/',views.registration,name='registration'),
    path('registration_student/',views.registration_student,name='registration_student'),
    path('registration_tutor/',views.registration_tutor,name='registration_tutor'),
    path('login/',views.login_page,name='login'),
    path('user_login',views.user_login,name="user_login"),
    path('user_logout',views.user_logout,name="user_logout"),
    path('editprofile', views.editprofile,name="editprofile"),  
    path('updateprofile/<int:id>', views.updateprofile,name='updateprofile'), 
    path('find',views.find,name='find'),
    path('question',views.question,name='question'),
    path('feedback',views.feedback,name='feedback'),
    path('material',views.material,name='material'),
    path('article',views.article,name='article'),
    path('forgetpassword',views.forgetpassword,name='forgetpassword'),
    path('article-details/<int:id>', views.article_details,name='article-details'),
    
    # path("resetpassword/",views.resetpassword,name="resetpassword"),
    # path("done/",views.resetpassworddone,name="resetpassworddone"),
    # path("resetpasswordconfirm/",views.resetpasswordconfirm,name="resetpasswordconfirm"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

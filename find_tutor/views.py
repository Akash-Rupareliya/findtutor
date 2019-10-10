from django.shortcuts import render,redirect
from .models import ArticleXcomment,Article,City,States,Student_Registration,Tutor_Registration,Category,Subject,Subcategory,Feedback,MasterUsers,Question,Material
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
import csv,io 

def search(request):
  if request.method=='POST':
    text='akash'
  

#this function is used for upload material to the database
def material(request):
  if request.method=='POST':
    mat_subject=request.POST.get('mat_subject')
    mat_doc=request.FILES['mat_doc']
    mat_user_id=request.POST.get('mat_user_id')
    insert=Material(mat_subject=mat_subject,mat_doc=mat_doc,mat_user_id=mat_user_id)
    insert.save()
  
    user=Material.objects.all()
    return redirect('material')
  else:
    user=Material.objects.all()
    return render(request,'material.html',{'user':user})


def register_user(request):
    if request.method=='POST':
        return render(request,'register.html',{})
    else:
        #context=['error']
        return render(request,'login.html',{})
        print("Error")

#this function check the session for admin is session is authorized the go to home page otherwise go to login page
def adminlogin(request):
  if request.session[request.user.username] is None:
    return render(request,'admintemplate/login.html')
  else:
    return render(request,'admintemplate/home.html')

#this function is used for admin login and if username and password is authorize then go to home page otherwise redirect to the login page
def admin_login(request):
    context={}
    if request.method=='POST': 
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)        
        if user is not None:
            request.session[user.username] = username
            if user.is_active:
                login(request,user)
                user=username        
                master=MasterUsers.objects.count()
                print(master)
                return render(request,'admintemplate/home.html',{'name':username,'count':master})                
        else:
            context["error"]="Provide valid credentials !!!"
            return render(request,'admintemplate/login.html',context)
    else:
        return render(request,'admintemplate/login.html',context)

#this function is used to go index page in admin site and @login_require is to check login is authenticated then open otherwise it throw to the login form
@login_required(login_url='/admin_login')
def admin_index(request):
    master=MasterUsers.objects.count()
    return render(request,'admintemplate/home.html',{'count':master})
      
#this function is used to logout admin
@login_required(login_url='/admin_login')
def admin_logout(request):    
    logout(request)    
    return render(request,'admintemplate/login.html',{})
    
#this function calls the about view page
def about_page(request):
  return render(request,'about.html',{'username':user})

#this function calls contact view page
def contact_page(request):
    return render(request,'contact-us.html',{'username':user})

#this function is used to go index page
def user_index(request):
    return render(request,'index.html',)

#this function is used to redirect user login page
def login_page(request):
     return render(request,'login.html')

def find(request):
    users=MasterUsers.objects.filter('user_name')
    return render(request,'find.html',{'users',users})

#this function is used to add city dynamically from admin side
@login_required(login_url='/admin_login')
def addcity(request):
    if request.method=='POST':
        # city=City()
        city_name=request.POST.get('cityname')
        state_id=request.POST.get('state_id')
        insert=City(city_name=city_name,state_id=state_id)
        states=States.objects.all()
        insert.save()
        return render(request,'admintemplate/addcity.html',{'states':states})
    else:
        states=States.objects.all()
        return  render(request,'admintemplate/addcity.html',{'states' : states})

#this function is used to give store feedback which can be given by student or users
def feedback(request):
    if request.method=='POST':
        feedback_name=request.POST.get('feedback_name')
        feedback_email=request.POST.get('feedback_email')
        feedback_mnum=request.POST.get('feedback_mnum')
        feedback_feedback=request.POST.get('feedback_feedback')
        insert=Feedback(feedback_name=feedback_name,feedback_email=feedback_email,feedback_mnum=feedback_mnum,feedback_feedback=feedback_feedback)
        insert.save()
        return render(request,'contact-us.html',{})

#this function is used to register tutor
def registration_tutor(request):
    if request.method=='POST':
        tutor_fname=request.POST.get('tutor_fname')
        tutor_lname=request.POST.get('tutor_lname')
        tutor_dob=request.POST.get('tutor_dob')
        tutor_mnum=request.POST.get('tutor_mnum')
        tutor_qualification=request.POST.get('tutor_qualification')
        tutor_experience=request.POST.get('tutor_experience')
        tutor_aboutme=request.POST.get('tutor_aboutme')
        tutor_gender=request.POST.get('tutor_gender')
        tutor_propic=request.FILES['tutor_propic']
        tutor_city_id=request.POST.get('tutor_city_id')
        tutor_state_id=request.POST.get('tutor_state_id')
        tutor_status='1'
        tutor_sub_id=request.POST.get('tutor_sub_id')
        master=MasterUsers.objects.order_by('-user_id').first()
        print(master)
        tutor_user_id=master.user_id
        insert=Tutor_Registration(tutor_fname=tutor_fname,tutor_lname=tutor_lname,tutor_mnum=tutor_mnum,tutor_gender=tutor_gender,tutor_dob=tutor_dob,tutor_qualification=tutor_qualification,tutor_experience=tutor_experience,tutor_aboutme=tutor_aboutme,tutor_propic=tutor_propic,tutor_status=tutor_status,tutor_city_id=tutor_city_id,tutor_state_id=tutor_state_id,tutor_user_id=tutor_user_id,tutor_sub_id=tutor_sub_id)
        insert.save()
        return render(request,'login.html',{})
    else:
        #context=['error']
        city=City.objects.all()
        states=States.objects.all()
        subject=Subject.objects.all()
        return render(request,'registration_tutor.html',{'states':states,'city':city,'subject':subject})
        #print("Error")

#this function is used for forget password using security question and answer
def forgetpassword(request):
    if request.method == 'POST':
        email=request.POST.get('user_email')
        sec_que=request.POST.get('sec_que')
        sec_ans=request.POST.get('sec_ans')
        password=request.POST.get('user_password')
        # print(email,sec_ans,sec_que,password)
        MasterUsers.objects.filter(user_email=email,sec_que=sec_que,sec_ans=sec_ans).update(user_pass=password)
        return redirect(user_login)
    return render(request, 'forgetpassword.html',{})

#this function is used for register in master table fields
def registration(request):
  if request.method=='POST':
    #  form = UserForm(request.POST)
      user_name=request.POST.get('user_name')
      user_email=request.POST.get('user_email')
      user_pass=request.POST.get('user_password')
      user_type=request.POST.get('user_type')
      sec_que=request.POST.get('sec_que')
      sec_ans=request.POST.get('sec_ans')
      insert=MasterUsers(user_name=user_name,user_email=user_email,user_pass=user_pass,user_type=user_type,sec_que=sec_que,sec_ans=sec_ans)
      insert.save()
      states = States.objects.all()
      city=City.objects.all()
      subject=Subject.objects.all()
      try:
        subject="Confirmation Mail"
        message="You Are Successfully Register with Find Tutor and Your Username Is : "+user_name +" And Your Password Is : "+user_pass
        from_mail=settings.EMAIL_HOST_USER
        to_list=[insert.user_email]
        s=send_mail(subject,message,from_mail,to_list)
        print(s)
        print(from_mail)  
      except Exception as e:
        print(e)
      if user_type=='student':

        return render(request,'registration_student.html',{'states' : states,'city':city,'subject':subject})
      elif user_type=='tutor':
        subject=Subject.objects.all()
        return render(request,'registration_tutor.html',{'states' : states,'city':city,'subject':subject})  
      else:
        return render(request,'registration_student.html')
      #return render(request,'login.html',{})
  else:
      return render(request,'registration.html')

#this function is used to redirect to edit profile view page
def editprofile(request):
    user=MasterUsers.objects.get(user_name=request.session['user_name'])
    return  render(request,'editprofile.html',{'user':user})

#this function is used for update profile after login
def updateprofile(request,id):
     if request.method=='POST':
        user_email=request.POST.get('user_email')
        user_name=request.POST.get('user_name')
        user_password=request.POST.get('user_password')
        user_type=request.POST.get('user_type')
        try:
            updateuser = MasterUsers(user_id=id,user_name=user_name,user_email=user_email,user_pass=user_password,user_type=user_type)
            updateuser.save()
            return redirect('user_index')
        except:
            return redirect('user_index')


#this function is used for article insert in article table
def article(request):
  if request.method=='POST':  
    art_title=request.POST.get('art_title')
    art_desc=request.POST.get('art_desc')
    art_user_id=request.POST.get('art_user_id')
    insert=Article(art_title=art_title,art_desc=art_desc,art_user_id=art_user_id)
    insert.save()
    return render(request,'articles.html',)
  else:
    article=Article.objects.all()
    return render(request,'articles.html',{'article':article})

#this function is used to redirect article details view from article view
def article_details(request,id):
  article=Article.objects.get(art_id=id)
  art_cmt=ArticleXcomment.objects.filter(artxcmt_art_id=article.art_id)
  return render(request,'article-details.html',{'article':article,'art_cmt':art_cmt})

#this function is used to insert question from student site
def question(request):
  if request.method=='POST':
    que_que=request.POST.get('que_que')
    que_user_id=request.POST.get('que_user_id')
    insert=Question(que_que=que_que,que_user_id=que_user_id)
    insert.save()
    return redirect(question)
  else:
    return render(request,'question.html')

#this function is used for student registration after filling registration form
def registration_student(request):
  if request.method=='POST':
      master=MasterUsers.objects.order_by('-user_id').first()
      stud_user_id=master.user_id
      stud_fname=request.POST.get('stud_fname')
      stud_lname=request.POST.get('stud_lname')
      stud_mnum=request.POST.get('stud_mnum')
      stud_gender=request.POST.get('stud_gender')
      stud_dob=request.POST.get('stud_dob')
      stud_propic=request.FILES['stud_propic']
      stud_state_id=request.POST.get('stud_state_id')
      stud_subcat_id=request.POST.get('stud_subcat_id')
      stud_city_id=request.POST.get('stud_city_id')
      insert=Student_Registration(stud_user_id=stud_user_id,stud_fname=stud_fname,stud_lname=stud_lname,stud_mnum=stud_mnum,stud_gender=stud_gender,stud_dob=stud_dob,stud_propic=stud_propic,stud_state_id=stud_state_id,stud_subcat_id=stud_subcat_id,stud_city_id=stud_city_id)
      
      insert.save()
      return render(request,'login.html',{})
  else:
      #context=['error']
      states = States.objects.all()
      city=City.objects.all()
      subject=Subject.objects.all()
      subcategory=Subcategory.objects.all()
      return render(request,'registration_student.html',{'states' : states,'city':city,'subject':subject,'subcategory':subcategory})


#this functio is used for user login
user=""
def user_login(request):
    
    context={}
    if request.method=='POST': 
        email=request.POST.get('email')
        password=request.POST.get('password')     
        login_obj=MasterUsers.objects.get(user_email=email,user_pass=password)
        
        if email==login_obj.user_email and password==login_obj.user_pass:
            if email is not None:
              request.session['email'] = login_obj.user_email
              request.session['type'] = login_obj.user_type
              request.session['user_name']=login_obj.user_name
              request.session['user_id']=login_obj.user_id
              return redirect('user_index')                    
            else:
              context["error"]="Provide valid credentials !!!"
              return render(request,'login.html',context)  
        else:
            context["error"]="Provide valid credentials !!!"
            return render(request,'login.html',context)
    else:
        return render(request,'index.html')
        
#this function is used for user logout 
def user_logout(request):    
    try:
      del request.session['email']
    except KeyError:
      pass
    return redirect('login')

#this function is used for insert city from admin site
@login_required(login_url='/admin_login')
def admin_addcity(request):
    states = States.objects.all()
    return render(request,'admintemplate/addcity.html',{'states' : states})

#this function is used for insert category
@login_required(login_url='/admin_login')
def addcategory(request):
  if request.method=='POST':
    category_name=request.POST.get('categoryname')      
    insert=Category(cat_name=category_name)
    insert.save()
    return render(request,'admintemplate/addcategory.html',{})
  else:
    return render(request,'admintemplate/addcategory.html',{})

#this function is used for insert subcategory
@login_required(login_url='/admin_login')
def addsubcategory(request):
  if request.method=='POST':
    subcat_name=request.POST.get('subcat_name')
    subcat_cat_id=request.POST.get('cat_id')      
    insert=Subcategory(subcat_name=subcat_name,subcat_cat_id=subcat_cat_id)
    category=Category.objects.all()
    insert.save()
    
    return render(request,'admintemplate/addsubcategory.html',{'category':category})
  else:
    category=Category.objects.all()
    return render(request,'admintemplate/addsubcategory.html',{'category': category})

#this function is used for insert subject
@login_required(login_url='/admin_login')
def addsubject(request):
  if request.method=='POST':
    sub_name=request.POST.get('subjectname') 
    sub_subcat_id=request.POST.get('sub_subcat_id')     
    subcategory=Subcategory.objects.all()
    insert=Subject(sub_name=sub_name,sub_subcat_id=sub_subcat_id)
    
    insert.save()
    return render(request,'admintemplate/addsubject.html',{'subcategory': subcategory})
  else:
    subcategory=Subcategory.objects.all()
    return render(request,'admintemplate/addsubject.html',{'subcategory': subcategory})

#this function is used for insert state
@login_required(login_url='/admin_login')
def addstate(request):
  if request.method=='POST':
    state_name=request.POST.get('state_name')      
    insert=States(state_name=state_name)
    insert.save()
    return redirect(addstate)
  else:
    state=States.objects.all()
    return render(request,'admintemplate/addstate.html',{'state':state})

#this function is used for view inserted registered user from admin side
@login_required(login_url='/admin_login')
def viewregisteredusers(request):
    users=MasterUsers.objects.all()
    return render(request,'admintemplate/viewregisteredusers.html',{'users':users})

#this function is used for view inserted category from admin side
@login_required(login_url='/admin_login')
def viewcategory(request):
    category=Category.objects.all()
    return render(request,'admintemplate/viewcategory.html',{'category':category})

#this function is used for upload bulk category in category table
@login_required(login_url='/admin_login')
def upload_csv_category(request):
  category=Category.objects.all()
  csv_file=request.FILES['document']
  if not csv_file.name.endswith('.csv'):
    message.error(request,"This File Is Not Csv")
    return HttpResponsRedirect('./')
  
  data_set = csv_file.read().decode('UTF-8')
  io_string=io.StringIO(data_set)
  
  for col in csv.reader(io_string,delimiter=','):
    _, created=Category.objects.update_or_create(
      cat_name=col[0]
    )

  return redirect(viewcategory)

#this function is used for upload bulk states in state table
@login_required(login_url='/admin_login')
def upload_csv(request):
  state=States.objects.all()
  csv_file=request.FILES['document']
  if not csv_file.name.endswith('.csv'):
    message.error(request,"This File Is Not Csv")
    return HttpResponsRedirect('./')
  
  data_set = csv_file.read().decode('UTF-8')
  io_string=io.StringIO(data_set)
  
  for col in csv.reader(io_string,delimiter=','):
    _, created=States.objects.update_or_create(
      state_name=col[0]
    )

  return redirect(viewstate)
  #return render(request,'admintemplate/viewstate.html')

#this function is used for view inserted states
@login_required(login_url='/admin_login')
def viewstate(request):
    state=States.objects.all()
    return render(request,'admintemplate/viewstate.html',{'state':state})

#this function is used for view inserted tutor
@login_required(login_url='/admin_login')
def viewtutor(request):
    users=Tutor_Registration.objects.all()
    return render(request,'admintemplate/viewtutors.html',{'users':users})

#this function is used for view inserted students
@login_required(login_url='/admin_login')
def viewstudents(request):
    users=Student_Registration.objects.all()
    return render(request,'admintemplate/viewstudents.html',{'users':users})

#this function is used to delete users from admin side
@login_required(login_url='/admin_login')
def delete_user(request,id):
  try:
    data = MasterUsers.objects.get(user_id=id)
    data.delete()
    datas=MasterUsers.objects.all()
    #return show  
    return redirect(viewregisteredusers)
    # show = show_data(request) 
    # return show   
  except:
    data=MasterUsers.objects.all()
  #return  render(request,'admintemplate/viewregisteredusers.html',{'name':data})

#this function is used for delete students from admin side
@login_required(login_url='/admin_login')
def delete_stud(request,id):
    try:
        data = Student_Registration.objects.get(stud_id=id)
        data.delete()
        datas=Student_Registration.objects.all()
        return redirect('viewstudents')
    except:
        data=Student_Registration.objects.all()
        return render(request,'admintemplate/viewstudents.html',{'name':data})

#this function is used for delete tutor
@login_required(login_url='/admin_login')
def delete_tutor(request,id):
    try:
        data = Tutor_Registration.objects.get(tutor_id=id)
        data.delete()
        datas=Tutor_Registration.objects.all()
      #return show  
        return redirect('viewtutor')

        # show = show_data(request) 
        # return show   
    except:
        data=Tutor_Registration.objects.all()
        return  render(request,'admintemplate/viewtutor.html',{'name':data})
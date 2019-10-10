from django.db import models
from phone_field import PhoneField
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Register(models.Model):
    user_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    

    class Meta:
        db_table="register"

class States(models.Model):
    state_id=models.AutoField(primary_key=True)
    state_name=models.CharField(max_length=50)

    class Meta:
        db_table="state"

    def __str__(self):
        return str(self.state_name)

class City(models.Model):
    city_id=models.AutoField(primary_key=True)
    city_name=models.CharField(max_length=50)
    state=models.ForeignKey(States,on_delete=models.CASCADE)
    class Meta:
        db_table="city"

class MasterUsers(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=50)
    user_email=models.EmailField(max_length=100,unique=True)
    user_pass=models.CharField(max_length=50)
    user_type=models.CharField(max_length=10)
    sec_que=models.IntegerField()
    sec_ans=models.CharField(max_length=30)
    #user_propic=models.ImageField(upload_to="upload/")
    class Meta:
        db_table="masterusers"
class Category(models.Model):
    cat_id=models.AutoField(primary_key=True)
    cat_name=models.CharField(max_length=300)
    class Meta:
        db_table="category"


class Subcategory(models.Model):
    subcat_id=models.AutoField(primary_key=True)
    subcat_cat=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcat_name = models.CharField(max_length=300)

    class Meta:
        db_table="subcategory"


class Student_Registration(models.Model):
    
    stud_id=models.AutoField(primary_key=True)
    stud_user=models.ForeignKey(MasterUsers,on_delete=models.CASCADE)
    stud_fname = models.CharField(max_length=50)
    stud_lname = models.CharField(max_length=50)
    stud_mnum = PhoneField(max_length=12,null=False,blank=False)
    stud_gender=models.CharField(max_length=6)
    stud_dob=models.DateField(auto_now=False)
    stud_state= models.ForeignKey(States,on_delete=models.CASCADE)
    stud_city = models.ForeignKey(City,on_delete=models.CASCADE)
    stud_subcat_id = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    stud_propic=models.ImageField(upload_to="upload/")
    stud_status=models.BooleanField(default=True)
    class Meta:
        db_table="student_registration"

class Subject(models.Model):
    sub_id=models.AutoField(primary_key=True)
    sub_subcat=models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    sub_name = models.CharField(max_length=300)
    class Meta:
        db_table="subject"

class Tutor_Registration(models.Model):
    tutor_id = models.AutoField(primary_key=True)
    tutor_user=models.ForeignKey(MasterUsers,on_delete=models.CASCADE)
    tutor_fname = models.CharField(max_length=50)
    tutor_lname = models.CharField(max_length=50)
    tutor_mnum = PhoneField(max_length=12,null=False,blank=False)
    tutor_gender=models.CharField(max_length=5)
    tutor_dob=models.DateField(auto_now=False)
    tutor_state = models.ForeignKey(States,on_delete=models.CASCADE)
    tutor_city = models.ForeignKey(City,on_delete=models.CASCADE)
    tutor_qualification = models.CharField(max_length=20)
    tutor_experience= models.IntegerField()
    tutor_aboutme=models.CharField(max_length=200)
    tutor_propic=models.ImageField(upload_to="upload/")
    tutor_status=models.BooleanField(default=True)
    tutor_sub=models.ForeignKey(Subject,on_delete=models.CASCADE)    
    class Meta:
        db_table="tutor_registration"

class Question(models.Model):
    que_id=models.AutoField(primary_key=True)
    que_que=models.CharField(max_length=300)
    que_user=models.ForeignKey(MasterUsers,on_delete=models.CASCADE)

    class Meta:
        db_table="question"

class Answer(models.Model):
    ans_id=models.AutoField(primary_key=True)
    ans_user= models.ForeignKey(MasterUsers,on_delete=models.CASCADE)
    ans_que=models.ForeignKey(Question,on_delete=models.CASCADE)
    ans_ans=models.CharField(max_length=500)
    ans_image=models.ImageField(upload_to="upload/")
    class Meta:
        db_table="answer"

class Notifaction(models.Model):
    not_id=models.AutoField(primary_key=True)
    not_user= models.ForeignKey(MasterUsers,on_delete=models.CASCADE)
    not_notif=models.CharField(max_length=300)
    class Meta:
        db_table="notification"


class Message(models.Model):
    msg_id = models.AutoField(primary_key=True)
    msg_msg = models.CharField(max_length=300)
    msg_user = models.ForeignKey(MasterUsers,on_delete=models.CASCADE)
 
    class Meta:
        db_table="message"

class Material(models.Model):
    mat_id=models.AutoField(primary_key=True)
    mat_subject=models.CharField(max_length=50)
    mat_doc=models.FileField(upload_to='documents/')
    mat_user=models.ForeignKey(MasterUsers,on_delete=models.CASCADE)
    class Meta:
        db_table="material"

class TutorXsubject(models.Model):
    tutsub_id=models.AutoField(primary_key=True)
    tutsub_sub=models.ForeignKey(Subject,on_delete=models.CASCADE)
    tutsub_tutor = models.ForeignKey(Tutor_Registration,on_delete=models.CASCADE)
    class Meta:
        db_table="tutorXsubject"


class Article(models.Model):
    art_id=models.AutoField(primary_key=True)
    art_title=models.CharField(max_length=100)
    art_desc=models.CharField(max_length=500)
    # art_date=models.DateField(default=datetime.now)
    art_user=models.ForeignKey(MasterUsers,on_delete=models.CASCADE)
    created_at=models.DateField(default=datetime.now)
    # models.DateField(default=timezone.now)
    class Meta:
        db_table="article"


class ArticleXcomment(models.Model):
    artxcmt_id=models.AutoField(primary_key=True)
    artxcmt_art=models.ForeignKey(Article,on_delete=models.CASCADE)
    artxcmt_user=models.ForeignKey(MasterUsers,on_delete=models.CASCADE)
    artxcmt_cmt=models.CharField(max_length=500)

    class Meta:
        db_table="articleXcomment"


class Articlelike(models.Model):
    artlike_id=models.AutoField(primary_key=True)
    artlike_art=models.ForeignKey(Article,on_delete=models.CASCADE)
    artlike_user=models.ForeignKey(MasterUsers,on_delete=models.CASCADE)

    class Meta:
        db_table="articlelike"


class Follow(models.Model):
    flw_id=models.AutoField(primary_key=True)
    flw_user=models.ForeignKey(MasterUsers,on_delete=models.CASCADE)

    class Meta:
        db_table="follow"


class Feedback(models.Model):
    feedback_id=models.AutoField(primary_key=True)
    #feedback_user=models.ForeignKey(MasterUsers,on_delete=models.CASCADE)
    feedback_name=models.CharField(max_length=50)
    feedback_email=models.EmailField(max_length=100,unique=True)
    feedback_mnum=PhoneField(max_length=12,null=False,blank=False)
    feedback_feedback=models.CharField(max_length=300)
    #feedback_rate=models.IntegerField()
    
    class Meta:
        db_table="feedback"
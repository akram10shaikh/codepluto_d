from django.db import models
from django.contrib.auth.models import AbstractUser

import io
import os
from django.core.files.base import ContentFile
from django.conf import settings
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont



# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    user_type_choice = ((1,'Admin'),
                        (2,'Teacher'),
                        (3,'Student'))
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    user_type = models.IntegerField(choices=user_type_choice, default=1)
    phone_number = models.CharField(max_length=15,null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='M')
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    image = models.ImageField(upload_to='media/user/',null=True)

    def save(self, *args, **kwargs):

        if self.pk is None and self.password:  # Only hash new passwords
            self.set_password(self.password)


        from myapp.models import Teacher, Student

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            if self.user_type == 2:
                Teacher.objects.create(
                    user=self,
                    username=self.username,
                    full_name=f"{self.first_name} {self.last_name}",
                    first_name=self.first_name,
                    last_name=self.last_name,
                    email=self.email,
                    phone=self.phone_number,
                    gender=self.gender,
                    image=self.image
                )
            elif self.user_type == 3:
                Student.objects.create(
                    user=self,
                    username=self.username,
                    full_name=f"{self.first_name} {self.last_name}",
                    first_name=self.first_name,
                    last_name=self.last_name,
                    email=self.email,
                    phone=self.phone_number,
                    gender=self.gender,
                    image=self.image
                )



    def __str__(self):
        return self.email

class Courses(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    course_name = models.CharField(max_length=50,null=True)
    description = models.TextField(default='No description available')
    image = models.ImageField(upload_to='courseimage/')
    price = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    total_lectures = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True,null=True)

    def __str__(self):
        return self.course_name



class Teacher(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    username = models.CharField(max_length=50,null=True)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    full_name = models.CharField(max_length=50,null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15,null=True)
    Gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
       ('O', 'Others')
     )
    gender = models.CharField(max_length=10,choices=Gender_choices,null=True)
    degree = models.CharField(max_length=50,null=True)
    college = models.CharField(max_length=50,null=True)
    experience = models.CharField(max_length=50,null=True)
    language = models.CharField(max_length=50,null=True)
    image = models.ImageField(upload_to='teacher/')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.email

class Student(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    username = models.CharField(max_length=50,null=True)
    full_name = models.CharField(max_length=50,null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15,null=True)
    father_name = models.CharField(max_length=20,null=True)
    mother_name = models.CharField(max_length=29,null=True)
    parents_phone = models.CharField(max_length=12,null=True)
    Gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
       ('O', 'Others')
     )
    gender = models.CharField(max_length=10,choices=Gender_choices,null=True)
    image = models.ImageField(upload_to='student/')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    address = models.TextField(null=True)
    city = models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    country = models.CharField(max_length=100,null=True)
    role_choices = (
        ('software developer', 'Software Developer'),
        ('backend developer', 'Backend Developer'),
       ('frontend developer', 'Frontend Developer')
     )
    role = models.CharField(max_length=30,choices=role_choices,default='software developer',null=True)

    # Course infomation
    courses_ongoing = models.ManyToManyField(Courses,related_name='courses_ongoing')
    wish_list = models.ManyToManyField(Courses,related_name='wish_list')

    def __str__(self):
        return self.user.username


class GradeClass(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    grade_name = models.CharField(max_length=40,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.grade_name

class BookClass(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    full_name = models.CharField(max_length=30,null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField( max_length=15,null=True)
    country = models.CharField(max_length=40,null=True)
    selected_grade = models.CharField(max_length=50,null=True)
    selected_date = models.DateField(null=True)
    selected_time = models.TimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    completed = models.BooleanField(default="False",null=True)

    def __str__(self):
        return self.full_name

class Feedback(models.Model):
    user = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    text = models.TextField(null=True,default="Customer Review")
    course = models.ForeignKey(Courses,on_delete=models.CASCADE,null=True)
    rating = [
        (1,'Very Bad'),
        (2,'Bad'),
        (3,'Okay'),
        (4,'Good'),
        (5,'Excellent'),
    ]
    rating = models.IntegerField(choices=rating,default=3)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.user.username

class Enquiry(models.Model):
    name = models.CharField(max_length=50,null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=20,null=True)
    message = models.TextField()

    def __str__(self):
        return self.name

class Certificate(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    course_name = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)
    completion_date = models.DateTimeField(null=True)
    certificate_pdf = models.FileField(upload_to='certificate', blank=True, null=True)
    grade = models.CharField(max_length=100, null=True)
    certificate_code = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.username} Certificate for {self.course_name.course_name}"

    def save(self, *args, **kwargs):
        # Save initially so we get a valid ID
        if not self.pk:
            super().save(*args, **kwargs)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=landscape(A4))
        width, height = landscape(A4)

        student_name = self.user.full_name
        course = self.course_name.course_name
        completion_date_str = self.completion_date.strftime("%d %B %Y") if self.completion_date else "N/A"
        grade = self.grade or "N/A"
        certificate_code = self.certificate_code or "N/A"

        description = f'''This is to certify that {student_name} has successfully completed the
        course conducted by CodePluto. This certificate is awarded in
        recognition of their dedication and successful completion of the program on {completion_date_str}.'''

        # Background PNG
        bg_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'certificate.png')
        if os.path.exists(bg_path):
            p.drawImage(bg_path, 0, 0, width=width, height=height)

        # Fonts
        font_path = os.path.join(settings.BASE_DIR, 'myapp', 'fonts', 'DancingScript-Bold.ttf')
        pdfmetrics.registerFont(TTFont("DancingScript-Bold", font_path))

        # Header
        p.setFillColor("#041582")
        p.setFont("Helvetica-Bold", 28)
        p.drawCentredString(width / 2, height - 100, "CODEPLUTO (E-Learning Providers )")

        # Title
        p.setFont("Helvetica-Bold", 36)
        p.setFillColor(HexColor("#1a1a1a"))
        p.drawCentredString(width / 2, height - 190, "Certificate of Completion")

        # Student Name
        p.setFont("DancingScript-Bold", 32)
        p.setFillColor(HexColor("#041582"))
        p.drawCentredString(width / 2, height - 250, student_name)

        # Course
        p.setFillColor("Black")
        p.setFont("Helvetica", 20)
        p.drawCentredString(width / 2, height - 290, "has successfully completed the course")
        p.setFont("Helvetica-Bold", 22)
        p.drawCentredString(width / 2, height - 320, course)

        # Description
        p.setFont("Helvetica", 13)
        lines = description.split('\n')
        y = height - 350
        for line in lines:
            p.drawCentredString(width / 2, y, line.strip())
            y -= 25

        # Certificate Code - Top Right
        p.setFont("Helvetica", 12)
        p.setFillColor(HexColor("#555555"))
        p.drawRightString(width - 50, height - 50, f"Code: {certificate_code}")

        # Signature + Date/Grade Bottom Right
        signature_path = os.path.join(settings.BASE_DIR, "static", "images", "certificate", "sign.png")
        sig_x = width - 250
        sig_y = 100
        if os.path.exists(signature_path):
            p.drawImage(signature_path, sig_x, sig_y, width=120, height=50, preserveAspectRatio=True, mask='auto')
            p.setFont("Helvetica", 14)
            p.drawString(sig_x, sig_y - 15, "Director, CodePluto")

            p.setFont("Helvetica", 12)
            p.setFillColor(HexColor("#333333"))
            p.drawRightString(width - 60, sig_y - 40, f"Completed on: {completion_date_str}")
            p.drawRightString(width - 60, sig_y - 60, f"Grade: {grade}")

        # Finalize PDF
        p.showPage()
        p.save()
        buffer.seek(0)

        # Save PDF to FileField
        file_name = f"certificate_{self.user.username}_{self.pk}.pdf"
        self.certificate_pdf.save(file_name, ContentFile(buffer.read()), save=False)

        # Save the model instance finally
        super().save(*args, **kwargs)


class Badge(models.Model):
    user = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    badge_title = models.CharField(max_length=100, blank=True, null=True)
    BADGE_CHOICES = [
        ('Rising Star','Rising Star'),
        ('Certified Mentor', 'Certified Mentor'),
        ('Elite Educato', 'Elite Educato'),
        ('Master Coach','Master Coach'),
    ]
    badge_level = models.CharField(max_length=100, choices=BADGE_CHOICES,default="Rising Star")
    badge_points = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name} {self.badge_title}"

class Resources(models.Model):
    course = models.ForeignKey(Courses,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,null=True)
    pdf_file = models.FileField(upload_to='pdf_file/',null=True)
    video = models.FileField(upload_to='resources_video/',null=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.course.course_name

class Meeting(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meet_link = models.URLField(blank=True)
    recording_link = models.URLField(blank=True)
    google_event_id = models.CharField(max_length=255, blank=True, null=True)
    completed = models.BooleanField(default="False",null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.title

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def google_authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

from datetime import timedelta, datetime
from django.db import models
from django.core.exceptions import ValidationError

# Import the function for authentication
from myapp.google_api import google_authenticate  # Or wherever it's defined

class Enrollment(models.Model):
    user = models.ForeignKey('Student', on_delete=models.CASCADE, null=True)
    course = models.ForeignKey('Courses', on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, null=True)
    progress = models.IntegerField(null=True)
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    repeat_count = models.IntegerField(default=1)        # 🔹 New
    days_between = models.IntegerField(default=1)
    meet_link = models.URLField(blank=True, null=True)
    recording_link = models.URLField(blank=True, null=True)
    google_event_id = models.CharField(max_length=255, blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     created_event_successfully = False

    #     if not self.google_event_id and self.start_time and self.end_time:
    #         try:
    #             creds = google_authenticate()
    #             service = build('calendar', 'v3', credentials=creds)

    #             for i in range(self.repeat_count):
    #                 start = self.start_time + timedelta(days=i * self.days_between)
    #                 end = self.end_time + timedelta(days=i * self.days_between)

    #                 event = {
    #                     'summary': f"{self.title} - Session {i+1}" if self.repeat_count > 1 else self.title,
    #                     'description': self.description,
    #                     'start': {'dateTime': start.isoformat(), 'timeZone': 'UTC'},
    #                     'end': {'dateTime': end.isoformat(), 'timeZone': 'UTC'},
    #                     'conferenceData': {
    #                         'createRequest': {
    #                             'requestId': f"enroll-{i}-{int(datetime.now().timestamp())}",
    #                             'conferenceSolutionKey': {'type': 'hangoutsMeet'},
    #                         },
    #                     },
    #                 }

    #                 created_event = service.events().insert(
    #                     calendarId='primary',
    #                     body=event,
    #                     conferenceDataVersion=1
    #                 ).execute()

    #                 if i == 0:
    #                     self.meet_link = created_event.get('hangoutLink')
    #                     self.google_event_id = created_event.get('id')

    #                 Meeting.objects.create(
    #                     user=self.user.user if hasattr(self.user, 'user') else self.user,
    #                     teacher=self.teacher,
    #                     title=event['summary'],
    #                     description=self.description,
    #                     start_time=start,
    #                     end_time=end,
    #                     meet_link=created_event.get('hangoutLink'),
    #                     google_event_id=created_event.get('id')
    #                 )

    #             created_event_successfully = True

    #         except Exception as e:
    #             print(f"[ERROR] Google Meet creation failed: {e}")
    #             # Log error, but continue saving the enrollment without meet link
    #             # Optionally: notify user/admin via messages framework or logs

    #     super().save(*args, **kwargs)  # Always called


class Earnings(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE,null=True)
    amount = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.username} {self.amount}"

class Payment_Demo_Classes(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    phone_number = models.IntegerField(null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='M')
    amount = models.IntegerField(null=True)
    invoice = models.CharField(max_length=100,null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.amount}"


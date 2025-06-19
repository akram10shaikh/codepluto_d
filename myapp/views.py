from django.shortcuts import render,redirect,get_object_or_404
from myapp.models import *
from django.contrib.auth import authenticate,login,logout
from myapp.forms import *
import pandas as pd
from django.core.mail import send_mail
from django.utils.timezone import now,localtime
from datetime import datetime, date
import pygal
from pygal.style import Style
from django.utils import timezone
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

from django_countries import countries
from myapp.country_code import COUNTRY_STD_CODES

from django.db.models import Sum

from django.templatetags.static import static

# Create your views here.
def home(request):
    user_feedback = Feedback.objects.order_by('-rating','-created_at')[:4]
    data_file = Courses.objects.all()

    # Country code and STD code
    selected_code = "IN"
    selected_country = None
    std_code = None


    return render(request,'index.html',{
        'user_feedback':user_feedback,
        'data_file':data_file,
        "countries": COUNTRY_STD_CODES,
        "selected_code": selected_code,
        "selected_country": selected_country,
        "std_code": std_code,
        })

# Courses Page
def courses_page(request):
    return render(request,'courses.html')

# Curruculum page
def curriculum_page(request):
    return render(request,'curriculum.html')

# Booking Demo class
def bookdemoclass(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        grade = request.POST.get('grade')
        date = request.POST.get('date')
        time = request.POST.get('time')

        today_date = now().date()
        today_time = now().time()

        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time, "%H:%M").time()


        if date_obj >= today_date:
            if today_time <= time_obj:
                # Saving the data in the database
                data = BookClass.objects.create(full_name=name,email=email,country=country,phone_number=phone,selected_grade=grade,selected_date=date,selected_time=time)
                data.save()

                # Sending message to the user
                subject = "Booking Codepluto : Demo class is confirm"
                message = f"Demo Class is Booked \n\nName: {name}\nPhone: {phone}\nGrade: {grade}\nDate: {date}\nTime: {time}\n\nJoin the class on time"
                on_mail = "codepluto56@gmail.com"
                send_mail(subject,message,'codepluto56@gmail.com',[on_mail])

                # Saving the data in the google sheet
                client = gspread.authorize(creds)
                sheet = client.open("Demobooking").sheet1
                sheet.append_row([name, email, country, phone, grade, date, time])

                # message to the frontend
                message_bro = 'Booking demo class is successfull'
                user_feedback = Feedback.objects.order_by('-rating','-created_at')[:4]
                data_file = Courses.objects.all()
                return render(request,'index.html',{'message':message_bro,'user_feedback':user_feedback,'data_file':data_file})

            else:
                message = 'Select the proper time for booking the class'
                user_feedback = Feedback.objects.order_by('-rating','-created_at')[:4]
                data_file = Courses.objects.all()
                return render(request,'index.html',{'message':message,'user_feedback':user_feedback,'data_file':data_file})


        else:
            message = 'Select the proper data for booking the class'
            user_feedback = Feedback.objects.order_by('-rating','-created_at')[:4]
            data_file = Courses.objects.all()
            return render(request,'index.html',{'message':message,'user_feedback':user_feedback,'data_file':data_file})

# Login page
def login_page(request):
    return render(request,'login.html')

# Login access to the account
def login_access(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            if user.user_type == 3:
                login(request,user)
                return redirect('student_home')
            else:
                logout(request)
                msg = "Wrong username or password"
                return render(request,'login.html',{'message':msg})
        else:
            msg = "Wrong username or password"
            return render(request,'login.html',{'message':msg})
    msg = "Something went wrong"
    return render(request,'login.html',{'message':msg})

def logout_access(request):
    logout(request)
    return redirect('login_type')

def login_type(request):
    return render(request,'login_type.html')

# Contact Us Page
def contact_us(request):
    return render(request,'contact_us.html')

# Saving the contact
def contact_save(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        phone_number = request.POST.get('phone_number')

        # Saving the date in the database
        data = Enquiry.objects.create(name=name,email=email,message=message,phone_number=phone_number)
        data.save()

        # Sending information on the mail
        subject = "CodePluto - Query"
        message = f"Enquiry from student \n\nName: {name}\nEmail: {email}\nPhone: {phone_number}\nMessage : {message} \n\nConnect to the person soon"
        on_mail = "codepluto56@gmail.com"
        send_mail(subject,message,'codepluto56@gmail.com',[on_mail])

        message = "We will connect you soon. Hava a nice day"
        return render(request,'contact_us.html',{'message':message})

    else:
        return render(request,'contact_us.html',{'message':message})

# Student Pages
# Student Home Page
def student_home(request):
    # Todays class
    today = timezone.now().date()
    today_class = Meeting.objects.filter(user=request.user,start_time__date=today)

    now_time = timezone.now()
    # Upcomming class
    now = timezone.now()
    tomorrow = now + timedelta(days=1)
    upcoming_class = Meeting.objects.filter(
    user=request.user,
    start_time__gte=tomorrow
    ).order_by('start_time')[:2]


    # Course Enrolled
    student = Student.objects.get(user=request.user)
    course = Enrollment.objects.filter(user=student)

    return render(request,'student_home.html',
                  {
                      'today_class':today_class,
                      'upcoming_class':upcoming_class,
                      'courses':course,
                      'now_time':now_time,
                      })

# Student Certificate Page
def certificate_page(request):
    user = CustomUser.objects.get(username=request.user.username)
    student = Student.objects.get(user=user)
    data = Certificate.objects.filter(user=student)
    return render(request,'certificate.html',{'data':data})

# Student Project Page
def project_page(request):
    custom_colors = ['#4CAF50', "#2276f4"]
    custom_style = Style(
        background='white',
        plot_background='white',
        foreground='#333',
        foreground_strong='#000',
        foreground_subtle='#666',
        colors = custom_colors,
    )
    pie_chart = pygal.Pie(inner_radius=.6,style=custom_style)
    pie_chart.title = "Project Progress"
    pie_chart.add('Completed',40)
    pie_chart.add('Not Completed',60)
    chart_svg = pie_chart.render_data_uri()

    # Bar Chart
    custom_colorss = ['#001aff']
    custom_style_bar = Style(
        background='white',
        plot_background='white',
        foreground='#333',
        foreground_strong='#000',
        foreground_subtle='#666',
        colors = custom_colorss,
    )

    bar_chart = pygal.Bar(style=custom_style_bar)
    bar_chart.title="Working Days"

    bar_chart.add('29-03-2025',10)
    bar_chart.add('30-03-2025',4)
    bar_chart.add('31-03-2025',8)
    bar_chart.add('01-04-2025',3)
    bar_chart.add('02-04-2025',10)

    bar_chart_file = bar_chart.render_data_uri()
    return render(request,'projects.html',{"chart_svg": chart_svg,"bar_chart_file":bar_chart_file})

# Student Profile Page View
def profile_page(request):
    profile, created = Student.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = Profile_Form(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            print("Form is valid, saving...")
            form.save()
            return redirect('profile_page')
        else:
            print("Form is NOT valid:", form.errors)

    else:
        form = Profile_Form(instance=profile)
    return render(request,'profile.html',{'form':form,'profile':profile})

# Student Content Page
def student_content(request):
    student = Student.objects.get(user=request.user)
    enroll = Enrollment.objects.filter(user=student)
    enrolled_courses = Enrollment.objects.filter(user=student).values_list('course',flat=True)
    resources= Resources.objects.filter(course__in=enrolled_courses)
    resources_total = Resources.objects.filter(course__in=enrolled_courses).count()

    return render(request,'student_content.html',
                  {
                      'resources':resources,
                      'resource_total':resources_total,
                      'enroll':enroll,
                      })





from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, Color
from django.http import FileResponse
import io
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
def chec(request):

    student_name = "Shaikh Akram"
    course = "Full Stack Python Development"
    completion_date = "15 May 2025"
    grade = "A+"
    certificate_code = "X123422"
    description = f'''This is to certify that {student_name} has successfully completed the
    course conducted by CodePluto. This certificate is awarded in
    recognition of their dedication and successful completion of the program on {completion_date}.'''

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

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

    # Student name
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

    # === Certificate Code - Top Right ===
    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#555555"))
    p.drawRightString(width - 50, height - 50, f"Code: {certificate_code}")

    # === Signature ===
    signature_path = os.path.join(settings.BASE_DIR, "static", "images", "certificate", "sign.png")
    sig_x = width - 250
    sig_y = 100
    if os.path.exists(signature_path):
        p.drawImage(signature_path, sig_x, sig_y, width=120, height=50, preserveAspectRatio=True, mask='auto')
        p.setFont("Helvetica", 14)
        p.drawString(sig_x, sig_y - 15, "Director, CodePluto")

        # === Completion Date & Grade - Bottom Right ===
        p.setFont("Helvetica", 12)
        p.setFillColor(HexColor("#333333"))
        p.drawRightString(width - 60, sig_y - 40, f"Completed on: {completion_date}")
        p.drawRightString(width - 60, sig_y - 60, f"Grade: {grade}")

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"certificate_of_{student_name}.pdf")
# Teacher Pages

# Login page
def teacher_login(request):
    return render(request,'login_teacher.html')

# Teacher login access
def teacher_login_access(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            if user.user_type == 2:
                login(request,user)
                return redirect('teacher_home')
            else:
                logout(request)
                msg = "Wrong username or password"
                return render(request,'login_teacher.html',{'message':msg})
        else:
            msg = "Wrong username or password"
            return render(request,'login_teacher.html',{'message':msg})
    msg = "Something went wrong"
    return render(request,'login_teacher.html',{'message':msg})

def teacher_home(request):
    user_login = request.user.username
    user = Teacher.objects.get(username=user_login)
    total_enrollement = Enrollment.objects.filter(teacher=user).count()
    demo_class = BookClass.objects.filter(teacher=user).count()
    earning = Earnings.objects.filter(teacher=user).aggregate(total=Sum('amount'))['total'] or 0
    upcoming_classes = Meeting.objects.filter(teacher=user,start_time__gte=timezone.now()).order_by('start_time')
    feedbacks = Feedback.objects.filter(teacher=user)
    rating_total =Feedback.objects.filter(teacher=user).count()
    rating_5 = Feedback.objects.filter(teacher=user,rating=5).count()
    rating_4 = Feedback.objects.filter(teacher=user,rating=4).count()
    total_positive = rating_5 + rating_4
    rating = int(total_positive/rating_total*100)

    badge_points = Badge.objects.get(user=user)
    points = badge_points.badge_points
    if int(points) >= 750:
        image = static('images/teacher_profile_view/platinum.jpg')
    elif int(points) >= 500:
        image = static('images/teacher_profile_view/gold.jpg')
    elif int(points) >= 250:
        image = static('images/teacher_profile_view/sliver.jpg')
    elif int(points) >= 100:
        image = static('images/teacher_profile_view/bronze.jpg')
    else:
        image = static('images/teacher_profile_view/rising_star.png')



    return render(request,'teacher_home.html',{
        'rating':rating,
        'total_enrollement':total_enrollement,
        'demo_class':demo_class,
        'earning':earning,
        'upcomming_class':upcoming_classes,
        'feedbacks':feedbacks,
        'image':image,
        'user':user,
    })

def teacher_profile_page(request):
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=teacher, user=request.user)
        if form.is_valid():
            form.save()
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                request.user.set_password(new_password)
                request.user.save()
                # Optionally re-login user or display success message
            return redirect('teacher_login')
    else:
        form = TeacherProfileForm(instance=teacher, user=request.user)

    return render(request,'teacher/teacher_profile.html',{'form':form,'teacher': teacher})


def teacher_profile_view(request):
    user_login = request.user.username
    user = CustomUser.objects.get(username=user_login)
    teacher = Teacher.objects.get(user=user)
    enroll = Enrollment.objects.filter(teacher=teacher).count()
    session = Meeting.objects.filter(teacher=teacher).count()
    earning = Earnings.objects.filter(teacher=teacher).aggregate(total=Sum('amount'))['total'] or 0
    today = date.today()
    demo = BookClass.objects.filter(teacher=teacher).count()
    courses = Courses.objects.filter(user=user)
    videos = Resources.objects.filter(teacher=teacher)
    student_rating_total = Feedback.objects.filter(teacher=teacher).count()
    student_rating_5 = Feedback.objects.filter(teacher=teacher,rating=5).count()
    student_rating_4 = Feedback.objects.filter(teacher=teacher,rating=4).count()
    rating_5 = student_rating_5/student_rating_total*100
    rating_4 = 100 - rating_5
    demo = BookClass.objects.filter(teacher=teacher).count()
    demo_successful = BookClass.objects.filter(teacher=teacher,completed=True).count()
    demo_not_successful = BookClass.objects.filter(teacher=teacher,completed=False).count()
    demo_earning = Payment_Demo_Classes.objects.filter(teacher=teacher)
    total_demo_earning = demo_earning.aggregate(Sum('amount'))['amount__sum'] or 0

    demo_class = {
        'demo_total':demo,
        'demo_successful':demo_successful,
        'demo_not_successful':demo_not_successful,
        'total_demo_earning':total_demo_earning,
    }

    total_live_classes = Meeting.objects.filter(teacher=teacher).count()
    live_classes_compeleted =  Meeting.objects.filter(teacher=teacher,completed=True).count()
    live_classes_not_compeleted =  Meeting.objects.filter(teacher=teacher,completed=False).count()
    live_class = {
        'total_live_classes':total_live_classes,
        'live_classes_compeleted':live_classes_compeleted,
        'live_classes_not_compeleted':live_classes_not_compeleted,
    }

    badge_points = Badge.objects.get(user=teacher)
    points = badge_points.badge_points
    if int(points) >= 750:
        image = static('images/teacher_profile_view/platinum.jpg')
        l1 = "Completed 750+ hours of classes."
        l2 = "Exemplary in all aspects and leadership."
        l3 = "Mentors others and leads initiatives."
    elif int(points) >= 500:
        image = static('images/teacher_profile_view/gold.jpg')
        l1 = "Completed 500+ hours of classes."
        l2 = "Consistently receives positive feedback."
        l3 = "Leads curriculum improvement."
    elif int(points) >= 250:
        image = static('images/teacher_profile_view/sliver.jpg')
        l1 = "Completed 250+ hours of classes."
        l2 = "Demonstrates reliability and consistency."
        l3 = "Maintains student engagement well."
    elif int(points) >= 100:
        image = static('images/teacher_profile_view/bronze.jpg')
        l1 = "Completed 100+ hours of classes."
        l2 = "Maintains good performance and feedback."
        l3 = "On track for mentorship."
    else:
        image = static('images/teacher_profile_view/rising_star.png')
        l1 = "Just started teaching."
        l2 = "Gaining momentum and punctuality."
        l3 = "Enthusiastic contributor."

    return render(request,'teacher/teacher_profile_view.html',
                  {
                      'form':teacher,
                      'enroll':enroll,
                      'session':session,
                      'earning':earning,
                      'today':today,
                      'demo':demo,
                      'courses':courses,
                      'videos':videos,
                      'rating_5':rating_5,
                      'rating_4':rating_4,
                      'student_rating_5':student_rating_5,
                      'student_rating_4':student_rating_4,
                      'student_rating_total':student_rating_total,
                      'demo_class':demo_class,
                      'live_class':live_class,
                      'image':image,
                      'l1':l1,
                      'l2':l2,
                      'l3':l3
                      })

def demo_class_page(request):
    teacher = Teacher.objects.get(user=request.user)
    demo = BookClass.objects.filter(teacher=teacher).order_by('-created_at')
    return render(request,'teacher/demo_class_page.html',
                  {
                      'demo':demo,
                  })

def live_class_page(request):
    teacher = Teacher.objects.get(user=request.user)
    live_class = Meeting.objects.filter(teacher=teacher).order_by('-created_at')
    return render(request,'teacher/live_class_page.html',
                    {
                        'live_class':live_class,
                    })

def teacher_feedback_page(request):
    teacher = Teacher.objects.get(user=request.user)
    feedback = Feedback.objects.filter(teacher=teacher)
    return render(request,'teacher/teacher_feedback_page.html',
                  {'feedback':feedback})

def teacher_upcomming_class(request):
    teacher = Teacher.objects.get(user=request.user)
    upcomming_classes = Meeting.objects.filter(teacher=teacher,start_time__gte=timezone.now()).order_by('start_time')
    return render(request,'teacher/teacher_upcomming_class.html',
    {
        'upcomming_classes':upcomming_classes,
    })

# Google Meeting views
import os,pickle
from django.contrib import messages
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

def google_authenticate():
    creds = None
    token_path = 'token.pickle'

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentialss.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def create_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            creds = google_authenticate()
            service = build('calendar', 'v3', credentials=creds)

            start = form.cleaned_data['start_time'].isoformat()
            end = form.cleaned_data['end_time'].isoformat()

            event = {
                'summary': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'start': {'dateTime': start, 'timeZone': 'UTC'},
                'end': {'dateTime': end, 'timeZone': 'UTC'},
                'conferenceData': {
                    'createRequest': {
                        'requestId': 'meeting-1234',
                        'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                    },
                },
            }

            created_event = service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1
            ).execute()

            meet_link = created_event.get('hangoutLink')
            event_id = created_event.get('id')

            meeting = form.save(commit=False)
            meeting.meet_link = meet_link
            meeting.google_event_id = event_id
            meeting.save()

            return redirect('meeting_detail', meeting.id)
    else:
        form = MeetingForm()

    return render(request, 'gmeet/create_meeting.html', {'form': form})


def meeting_list(request):

    meetings = Meeting.objects.all().order_by('-start_time')
    return render(request, 'gmeet/meeting_list.html', {'meetings': meetings})


def meeting_detail(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    return render(request, 'gmeet/meeting_detail.html', {'meeting': meeting})


def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)

    if meeting.google_event_id:
        creds = google_authenticate()
        service = build('calendar', 'v3', credentials=creds)

        try:
            service.events().delete(calendarId='primary', eventId=meeting.google_event_id).execute()
            messages.success(request, "Meeting deleted from Google Calendar.")
        except Exception as e:
            messages.error(request, f"Failed to delete meeting: {e}")

    meeting.delete()
    return redirect('meeting_list')



def update_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            creds = google_authenticate()
            service = build('calendar', 'v3', credentials=creds)

            updated_event = {
                'summary': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'start': {
                    'dateTime': form.cleaned_data['start_time'].isoformat(),
                    'timeZone': 'Asia/Kolkata'
                },
                'end': {
                    'dateTime': form.cleaned_data['end_time'].isoformat(),
                    'timeZone': 'Asia/Kolkata'
                },
            }

            service.events().patch(
                calendarId='primary',
                eventId=meeting.google_event_id,
                body=updated_event
            ).execute()

            form.save()
            return redirect('meeting_detail', meeting.id)
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'gmeet/update_meeting.html', {'form': form, 'meeting': meeting})

import datetime
import os.path
from django.http import JsonResponse
from django.shortcuts import render
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_google_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def calendar_view(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            creds = google_authenticate()
            service = build('calendar', 'v3', credentials=creds)

            start = form.cleaned_data['start_time'].isoformat()
            end = form.cleaned_data['end_time'].isoformat()

            event = {
                'summary': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'start': {'dateTime': start, 'timeZone': 'UTC'},
                'end': {'dateTime': end, 'timeZone': 'UTC'},
                'conferenceData': {
                    'createRequest': {
                        'requestId': 'meeting-1234',
                        'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                    },
                },
            }

            created_event = service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1
            ).execute()

            meet_link = created_event.get('hangoutLink')
            event_id = created_event.get('id')

            meeting = form.save(commit=False)
            meeting.meet_link = meet_link
            meeting.google_event_id = event_id
            meeting.save()

            return render(request, 'calendar.html',{'form':form})
    else:
        form = MeetingForm()
    return render(request, 'teacher/calendar.html',{'form':form})

def google_calendar_events(request):
    teacher = Teacher.objects.get(user=request.user)  # Get the related Teacher
    meetings = Meeting.objects.filter(teacher=teacher)
    events = []

    for meeting in meetings:
        events.append({
            'id': meeting.google_event_id,  # <-- this is key!
            'title': meeting.title,
            'start': meeting.start_time.isoformat(),
            'end': meeting.end_time.isoformat(),
            'description': meeting.description,
            'meet_link': meeting.meet_link,
        })

    return JsonResponse(events, safe=False)

def delete_calendar_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, google_event_id=meeting_id)
    if meeting.google_event_id:
        creds = google_authenticate()
        service = build('calendar', 'v3', credentials=creds)

        try:
            service.events().delete(calendarId='primary', eventId=meeting.google_event_id).execute()
            messages.success(request, "Meeting deleted from Google Calendar.")
        except Exception as e:
            messages.error(request, f"Failed to delete meeting: {e}")

    meeting.delete()
    form = MeetingForm()
    return render(request, 'teacher/calendar.html',{'form':form})


def update_calendar_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, google_event_id=meeting_id)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            creds = google_authenticate()
            service = build('calendar', 'v3', credentials=creds)

            updated_event = {
                'summary': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'start': {
                    'dateTime': form.cleaned_data['start_time'].isoformat(),
                    'timeZone': 'Asia/Kolkata'
                },
                'end': {
                    'dateTime': form.cleaned_data['end_time'].isoformat(),
                    'timeZone': 'Asia/Kolkata'
                },
            }

            service.events().patch(
                calendarId='primary',
                eventId=meeting.google_event_id,
                body=updated_event
            ).execute()

            form.save()
            return render(request, 'teacher/calendar.html', {'form': form, 'meeting': meeting})
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'teacher/calendar.html', {'form': form, 'meeting': meeting})

def create_calendar_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            # Get the current logged-in user
            # user = request.user
            teacher = CustomUser.objects.get(username=request.user.username)
            user = Teacher.objects.get(user=teacher)

            creds = google_authenticate()
            service = build('calendar', 'v3', credentials=creds)

            start = form.cleaned_data['start_time'].isoformat()
            end = form.cleaned_data['end_time'].isoformat()

            event = {
                'summary': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'start': {'dateTime': start, 'timeZone': 'UTC'},
                'end': {'dateTime': end, 'timeZone': 'UTC'},
                'conferenceData': {
                    'createRequest': {
                        'requestId': 'meeting-1234',
                        'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                    },
                },
            }

            # Create the event in Google Calendar
            created_event = service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1
            ).execute()

            # Get the meeting link and event ID
            meet_link = created_event.get('hangoutLink')
            event_id = created_event.get('id')

            # Save the meeting to the database with the current user
            meeting = form.save(commit=False)
            meeting.teacher = user  # Assign the current user
            meeting.meet_link = meet_link
            meeting.google_event_id = event_id
            meeting.save()

            # Redirect or render the same page with success
            return redirect('calendar_page')  # Assuming you have a calendar page URL

    else:
        form = MeetingForm()

    return render(request, 'teacher/calendar.html', {'form': form})

from django.urls import path
from myapp.views import *

urlpatterns = [
    path('',home,name='home'),
    path('bookdemoclass/',bookdemoclass,name='bookdemoclass'),
    path('courses_page/',courses_page,name='courses_page'),
    path('curriculum_page/',curriculum_page,name='curriculum_page'),
    path('contact_us/',contact_us,name='contact_us'),
    path('contact_save/',contact_save,name='contact_save'),

    path('login_type/',login_type,name='login_type'),
    path('login_page/',login_page,name='login_page'),
    path('login_access/',login_access,name='login_access'),

    path('logout_access/',logout_access,name='logout_access'),

    # Student URLs
    # Student Home page
    path('student_home/',student_home,name='student_home'),

    # Certificate Page
    path('certificate_page/',certificate_page,name='certificate_page'),

    # Project Page
    path('project_page/',project_page,name='project_page'),

    # Profile Page
    path('profile_page/',profile_page,name='profile_page'),

    # Student Content Page
    path('student_content/',student_content,name='student_content'),

    # Teacher Pages
    # Teacher Login
    path('teacher_login/',teacher_login,name='teacher_login'),

    # Teacher Login access
    path('teacher_login_access/',teacher_login_access,name='teacher_login_access'),
    # Teacher Home page
    path('teacher_home/',teacher_home,name='teacher_home'),
    # Teacher Profile Page
    path('teacher_profile_page/',teacher_profile_page,name='teacher_profile_page'),
    # Teacher profile view
    path('teacher_profile_view/',teacher_profile_view,name='teacher_profile_view'),
    # Teacher Demo Class Page
    path('demo_class_page/',demo_class_page,name='demo_class_page'),
    # Teacher Live Class Page
    path('live_class_page/',live_class_page,name='live_class_page'),
    # Teacher Feedback page
    path('teacher_feedback_page/',teacher_feedback_page,name='teacher_feedback_page'),
    # Teacher Upcomming classes page
    path('teacher_upcomming_class/',teacher_upcomming_class,name='teacher_upcomming_class'),

    # Google Meeting URLs
    path('create/', create_meeting, name='create_meeting'),
    path('<int:meeting_id>/',meeting_detail, name='meeting_detail'),
    path('<int:meeting_id>/delete/',delete_meeting, name='delete_meeting'),
    path('meeting_list/',meeting_list,name='meeting_list'),
    path('meeting/<int:meeting_id>/edit/',update_meeting, name='update_meeting'),


    path('meetings/<str:meeting_id>/delete/', delete_calendar_meeting, name='delete_calender_meeting'),
    path('calendar/', calendar_view, name='calendar_page'),
    path('calendar/events/', google_calendar_events, name='calendar_events'),
    path('meeting/<str:meeting_id>/update/', update_calendar_meeting, name='update_calendar_meeting'),
    path('meetings/create/', create_calendar_meeting, name='create_calendar_meeting'),


    path('chec/',chec,name='chec'),
]


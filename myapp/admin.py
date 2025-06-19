from django.contrib import admin
from myapp.models import *

from myapp.forms import MeetingAdminForm
from myapp.google_api import google_authenticate
from googleapiclient.discovery import build
from datetime import timedelta

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(GradeClass)
admin.site.register(BookClass)
admin.site.register(Feedback)
admin.site.register(Enquiry)
admin.site.register(Courses)
admin.site.register(Certificate)

admin.site.register(Resources)


class MeetingAdmin(admin.ModelAdmin):
    form = MeetingAdminForm
    list_display = ['title', 'user', 'start_time', 'end_time', 'meet_link']
    list_filter = ['user', 'start_time']
    search_fields = ['title', 'description', 'meet_link']

    def save_model(self, request, obj, form, change):
        if not change:
            repeat_count = form.cleaned_data.get('repeat_count', 1)
            days_between = form.cleaned_data.get('days_between', 1)

            creds = google_authenticate()
            service = build('calendar', 'v3', credentials=creds)

            for i in range(repeat_count):
                start = obj.start_time + timedelta(days=i * days_between)
                end = obj.end_time + timedelta(days=i * days_between)

                event = {
                    'summary': f"{obj.title} - Session {i+1}",
                    'description': obj.description,
                    'start': {'dateTime': start.isoformat(), 'timeZone': 'UTC'},
                    'end': {'dateTime': end.isoformat(), 'timeZone': 'UTC'},
                    'conferenceData': {
                        'createRequest': {
                            'requestId': f"admin-bulk-{i}-{int(start.timestamp())}",
                            'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                        },
                    },
                }

                created_event = service.events().insert(
                    calendarId='primary',
                    body=event,
                    conferenceDataVersion=1
                ).execute()

                Meeting.objects.create(
                    user=obj.user,  # 🔸 Selected manually in the admin form
                    teacher=obj.teacher,
                    title=event['summary'],
                    description=obj.description,
                    start_time=start,
                    end_time=end,
                    meet_link=created_event.get('hangoutLink'),
                    google_event_id=created_event.get('id'),
                )
        else:
            super().save_model(request, obj, form, change)


admin.site.register(Meeting, MeetingAdmin)

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'start_time', 'end_time', 'meet_link']
    readonly_fields = ['meet_link', 'google_event_id']
    fields = [
        'user', 'course', 'teacher', 'progress',
        'title', 'description', 'start_time', 'end_time',
        'repeat_count', 'days_between',  # Add these
        'meet_link', 'recording_link', 'google_event_id'
    ]

    def save_model(self, request, obj, form, change):
    # Always save the Enrollment object first
        super().save_model(request, obj, form, change)

        if not change:
            repeat_count = form.cleaned_data.get('repeat_count', 1)
            days_between = form.cleaned_data.get('days_between', 1)

            try:
                creds = google_authenticate()
                service = build('calendar', 'v3', credentials=creds)

                for i in range(repeat_count):
                    start = obj.start_time + timedelta(days=i * days_between)
                    end = obj.end_time + timedelta(days=i * days_between)

                    event = {
                        'summary': f"{obj.title} - Session {i+1}",
                        'description': obj.description,
                        'start': {'dateTime': start.isoformat(), 'timeZone': 'UTC'},
                        'end': {'dateTime': end.isoformat(), 'timeZone': 'UTC'},
                        'conferenceData': {
                            'createRequest': {
                                'requestId': f"admin-bulk-{i}-{int(start.timestamp())}",
                                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                            },
                        },
                    }

                    created_event = service.events().insert(
                        calendarId='primary',
                        body=event,
                        conferenceDataVersion=1
                    ).execute()

                    # Save Meet info to Enrollment only for the first event
                    if i == 0:
                        obj.meet_link = created_event.get('hangoutLink')
                        obj.google_event_id = created_event.get('id')
                        obj.save()  # Save updates to the Enrollment instance

                    # Create Meeting instance
                    Meeting.objects.create(
                        user=obj.user.user if hasattr(obj.user, 'user') else obj.user,
                        teacher=obj.teacher,
                        title=event['summary'],
                        description=obj.description,
                        start_time=start,
                        end_time=end,
                        meet_link=created_event.get('hangoutLink'),
                        google_event_id=created_event.get('id'),
                    )
            except Exception as e:
                self.message_user(request, f"Google Meet creation failed: {e}", level='error')


    def delete_model(self, request, obj):
        if obj.google_event_id:
            try:
                creds = google_authenticate()
                service = build('calendar', 'v3', credentials=creds)
                service.events().delete(calendarId='primary', eventId=obj.google_event_id).execute()
                print(f"Deleted Google event {obj.google_event_id}")
            except Exception as e:
                print(f"Failed to delete Google event {obj.google_event_id}: {e}")
        super().delete_model(request, obj)

    # Handle bulk delete (checkbox action)
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.google_event_id:
                try:
                    creds = google_authenticate()
                    service = build('calendar', 'v3', credentials=creds)
                    service.events().delete(calendarId='primary', eventId=obj.google_event_id).execute()
                    print(f"Deleted Google event {obj.google_event_id}")
                except Exception as e:
                    print(f"Failed to delete Google event {obj.google_event_id}: {e}")
        super().delete_queryset(request, queryset)


admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Earnings)
admin.site.register(Payment_Demo_Classes)
admin.site.register(Badge)
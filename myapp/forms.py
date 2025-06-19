from django import forms
from myapp.models import *

class EnquiryForm(forms.Form):
    class Meta:
        model = Enquiry
        fields = '__all__'

class Profile_Form(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'parents_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'description', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class MeetingAdminForm(forms.ModelForm):
    repeat_count = forms.IntegerField(initial=1, required=False, help_text="Number of meetings to create")
    days_between = forms.IntegerField(initial=1, required=False, help_text="Days between each meeting")

    class Meta:
        model = Meeting
        fields = '__all__'


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'gender': forms.Select(choices=Teacher.Gender_choices),
        }

    # Optional: Customize file input widget for image
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))



class TeacherProfileForm(forms.ModelForm):
    current_password = forms.CharField(
        label="Current Password", required=False,
        widget=forms.PasswordInput()
    )
    new_password = forms.CharField(
        label="New Password", required=False,
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label="Confirm New Password", required=False,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = Teacher
        fields = [
            'username', 'first_name', 'last_name', 'full_name',
            'email', 'phone', 'gender', 'degree', 'college',
            'experience', 'language', 'image'
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password or confirm_password:
            if not current_password:
                self.add_error('current_password', "Enter your current password.")
            elif not self.user.check_password(current_password):
                self.add_error('current_password', "Current password is incorrect.")
            elif new_password != confirm_password:
                self.add_error('confirm_password', "New passwords do not match.")

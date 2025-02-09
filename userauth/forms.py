from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("instructor", "Instructor"),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial="student", required=True, label="Role")
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists!")
        return email

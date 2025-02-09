from django.contrib import messages
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import CustomUserCreationForm


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        role = form.cleaned_data.get("role")

        if role == "student":
            group, created = Group.objects.get_or_create(name="Students")
        elif role == "instructor":
            group, created = Group.objects.get_or_create(name="Instructors")
        else:
            group = None

        if group:
            user.groups.add(group)

        messages.success(self.request, "Ypu registered successfully!")
        return super().form_valid(form)

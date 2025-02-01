from django import forms

from .models import Course, CoursePart, CourseTopic, TopicDocument


class CourseForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255, required=True, label="Course Title", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Enter course description..."}),
    )

    class Meta:
        model = Course
        fields = ["title", "description"]


class PartForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        required=True,
        label="Part Title",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter part title"}),
    )
    course_id = forms.CharField(max_length=255, required=True, widget=forms.HiddenInput())

    class Meta:
        model = CoursePart
        fields = ["title", "course_id"]


class TopicForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        required=True,
        label="Topic Title",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter topic title"}),
    )
    part_id = forms.CharField(max_length=255, required=True, widget=forms.HiddenInput())

    class Meta:
        model = CourseTopic
        fields = ["title", "part_id"]


class TopicDocumentForm(forms.ModelForm):
    topic = forms.ModelChoiceField(queryset=CourseTopic.objects.all(), empty_label="Select a topic", required=True)

    class Meta:
        model = TopicDocument
        fields = ["name", "file", "topic"]

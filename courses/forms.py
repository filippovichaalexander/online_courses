from django import forms
from .models import TopicDocument, Course, CoursePart, CourseTopic


class CourseForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Course
        fields = ['title']


class PartForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=True)
    course_id = forms.CharField(max_length=255, required=True, widget=forms.HiddenInput())

    class Meta:
        model = CourseTopic
        fields = ['title', 'course_id']


class TopicForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=True)
    course_title = forms.CharField(max_length=255, required=True, widget=forms.HiddenInput())
    part_title = forms.CharField(max_length=255, required=True, widget=forms.HiddenInput())

    class Meta:
        model = CourseTopic
        fields = ['title', 'course_title', 'part_title']


class TopicDocumentForm(forms.ModelForm):
    topic = forms.ModelChoiceField(
        queryset=CourseTopic.objects.all(),
        empty_label="Select a topic",
        required=True
    )

    class Meta:
        model = TopicDocument
        fields = ['name', 'file', 'topic']

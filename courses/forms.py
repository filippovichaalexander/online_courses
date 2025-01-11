from django import forms
from .models import TopicDocument, Course, CoursePart, CourseTopic

class CourseForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=True)
    # part = forms.ModelChoiceField(
    #     queryset=CoursePart.objects.all(),
    #     empty_label="Select a course part",
    #     required=True
    # )
    # topic = forms.ModelChoiceField(
    #     queryset=CourseTopic.objects.all(),
    #     empty_label="Select a part topic",
    #     required=True
    # )
    class Meta:
        model = Course
        fields = ['title']

class TopicDocumentForm(forms.ModelForm):
    topic = forms.ModelChoiceField(
        queryset=CourseTopic.objects.all(),
        empty_label="Select a topic",
        required = True
    )

    class Meta:
        model = TopicDocument
        fields = ['name', 'file', 'topic']


from django import forms
from .models import TopicDocument, CourseTopic


class TopicDocumentForm(forms.ModelForm):
    topic = forms.ModelChoiceField(
        queryset=CourseTopic.objects.all(),
        empty_label="Select a topic",
        required = True
    )

    class Meta:
        model = TopicDocument
        fields = ['name', 'file', 'topic']
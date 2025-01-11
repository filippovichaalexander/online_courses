from django.shortcuts import render, redirect, get_object_or_404

from .forms import TopicDocumentForm, CourseForm
from .models import Course, CoursePart, CourseTopic, TopicDocument


def courses_list(request):
    courses = Course.objects.all()  # Fetching TopicDocument instances
    parts = CoursePart.objects.all()
    topics = CourseTopic.objects.all()

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Make sure to have a success URL
    else:
        form = CourseForm()  # Initialize the form for GET request

    context = {
        'form': form,  # Include the form in the context
        'courses': courses,
        # 'parts': parts,
        # 'topics': topics
    }
    return render(request, 'courses_list.html', context)

def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    parts = course.parts.all()
    topics = CourseTopic.objects.filter(part__course=course)

    context = {
        'course': course,
        'parts': parts,
        'topics': topics,
    }
    return render(request, 'course_details.html', context)

def part_details(request, course_id, part_id):
    part = CoursePart.objects.get(id=part_id)
    course = Course.objects.get(id=course_id)
    topics = CourseTopic.objects.all()

    context = {
        'part': part,
        'course': course,
        'topics': topics,
    }
    return render(request, 'part_details.html', context)

def update_course(request, course_id):
    course = get_object_or_404(CourseForm, id=course_id)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'update_course.html', {'form': form})


def delete_course(request, course_id):
    course = get_object_or_404(CourseForm, id=course_id)

    if request.method == 'POST':
        # delete file itself
        # if document.file:
        #     document.file.delete(save=False)
        # delete db row
        course.delete()
        return redirect('courses_list')


def update_part(request, part_id):
    part = get_object_or_404(CoursePart, id=part_id)

    if request.method == 'POST':
        form = CoursePart(request.POST, instance=part)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CoursePart(instance=part)

    return render(request, 'update_part.html', {'form': form})


def delete_part(request, part_id):
    part = get_object_or_404(CourseTopic, id=part_id)

    if request.method == 'POST':
        # delete file itself
        # if document.file:
        #     document.file.delete(save=False)
        # delete db row
        part.delete()
        return redirect('courses_list')

    return render(request, 'confirm_delete.html', {'part': part})


def update_topic(request, topic_id):
    topic = get_object_or_404(CourseTopic, id=topic_id)

    if request.method == 'POST':
        form = CourseTopic(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseTopic(instance=topic)

    return render(request, 'update_topic.html', {'form': form})


def delete_topic(request, topic_id):
    topic = get_object_or_404(CourseTopic, id=topic_id)

    if request.method == 'POST':
        # delete file itself
        # if document.file:
        #     document.file.delete(save=False)
        # delete db row
        topic.delete()
        return redirect('courses_list')

    return render(request, 'confirm_delete.html', {'topic': topic})


# documents
def document_list(request):
    if request.method == 'POST':
        form = TopicDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = TopicDocumentForm()

    documents = TopicDocument.objects.all()
    return render(request, 'document_list.html', {'form': form, 'documents': documents})


def update_document(request, document_id):
    document = get_object_or_404(TopicDocument, id=document_id)

    if request.method == 'POST':
        form = TopicDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = TopicDocumentForm(instance=document)

    return render(request, 'update_document.html', {'form': form, 'document': document})


def delete_document(request, document_id):
    document = get_object_or_404(TopicDocument, id=document_id)

    if request.method == 'POST':
        # delete file itself
        # if document.file:
        #     document.file.delete(save=False)
        # delete db row
        document.delete()
        return redirect('document_list')

    return render(request, 'confirm_delete.html', {'document': document})

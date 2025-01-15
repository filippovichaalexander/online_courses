from django.shortcuts import render, redirect, get_object_or_404

from .forms import TopicDocumentForm, CourseForm, PartForm, TopicForm
from .models import Course, CoursePart, CourseTopic, TopicDocument


def courses_list(request):
    courses = Course.objects.all().order_by('id')
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = CourseForm()

    context = {
        'form': form,
        'courses': courses,
    }
    return render(request, 'courses_list.html', context)


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    parts = course.parts.all()

    if request.method == 'POST':
        form = PartForm(request.POST, initial={'course_title': course.title})
        if form.is_valid():
            part = form.save(commit=False)
            part.course = course
            part.save()
            return redirect('success')
    else:
        form = PartForm(initial={'course_title': course.title})

    context = {
        'form': form,
        'course': course,
        'parts': parts,
    }
    return render(request, 'course_details.html', context)


def part_details(request, course_id, part_id):
    part = get_object_or_404(CoursePart, id=part_id)
    course = get_object_or_404(Course, id=course_id)
    topics = part.topics.all()

    if request.method == 'POST':
        form = PartForm(request.POST, instance={'course_title': course.title, 'part_title': part.title})
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = PartForm(instance={'course_title': course.title, 'part_title': part.title})

    context = {
        'form': form,
        'part': part,
        'course': course,
        'topics': topics,
    }
    return render(request, 'part_details.html', context)


def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses_list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'update_course.html', {'form': form})


def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        # delete file itself
        # if document.file:
        #     document.file.delete(save=False)
        # delete db row
        course.delete()
        return redirect('courses_list')
    else:
        # Render a confirmation template or redirect to the courses_list view
        return render(request, 'confirm_delete_course.html', {'course': course})


def update_part(request, part_id):
    part = get_object_or_404(CoursePart, id=part_id)
    course = get_object_or_404(Course, id=part.course.id)

    if request.method == 'POST':
        form = PartForm(request.POST, instance=part)
        if form.is_valid():
            part = form.save(commit=False)
            part.course = course
            part.save()
            return redirect('course_details', course_id=course.id)
    else:
        form = PartForm(instance=part, initial={'course_title': course.title})

    context = {
        'form': form,
        'part': part,
        'course': course,
    }
    return render(request, 'update_part.html', context)


def delete_part(request, part_id):
    part = get_object_or_404(CoursePart, id=part_id)
    course_id = part.course.id

    if request.method == 'POST':
        # delete file itself
        # if document.file:
        #     document.file.delete(save=False)
        # delete db row
        part.delete()
        return redirect('course_details', course_id=course_id)

    return render(request, 'confirm_delete_part.html', {'part': part})


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

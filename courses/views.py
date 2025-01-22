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
        part_form = PartForm(request.POST)
        if part_form.is_valid():
            part = part_form.save(commit=False)
            part.course = course
            part.save()
            return redirect('success')
    else:
        part_form = PartForm(initial={'course_id': course.id})

    context = {
        'part_form': part_form,
        'course': course,
        'parts': parts,
    }
    return render(request, 'course_details.html', context)


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


def part_details(request, course_id, part_id):
    part = get_object_or_404(CoursePart, id=part_id)
    course = get_object_or_404(Course, id=course_id)
    topics = part.topics.all()

    if request.method == 'POST':
        topic_form = TopicForm(request.POST)
        if topic_form.is_valid():
            topic = topic_form.save(commit=False)
            topic.part = part
            topic.save()
            return redirect('success')
    else:
        topic_form = TopicForm(initial={'part_id': part.id})

    context = {
        'topic_form': topic_form,
        'part': part,
        'course': course,
        'topics': topics,
    }
    return render(request, 'part_details.html', context)


def create_course_part(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        part_form = PartForm(request.POST)
        if part_form.is_valid():
            part = part_form.save(commit=False)
            part.course = course
            part.save()
            return redirect('part_details', course_id=course.id, part_id=part.id)
    else:
        part_form = PartForm(initial={'course_id': course.id})

    context = {
        'part_form': part_form,
        'course': course,
    }
    return render(request, 'create_course_part.html', context)


def update_part(request, part_id):
    part = get_object_or_404(CoursePart, id=part_id)
    course = get_object_or_404(Course, id=part.course.id)

    if request.method == 'POST':
        form = PartForm(request.POST, instance=part)
        if form.is_valid():
            form.save()
            return redirect('course_details', course_id=course.id)
    else:
        form = PartForm(instance=part, initial={'course_id': course.id})

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
    part = get_object_or_404(CoursePart, id=topic.part.id)

    if request.method == 'POST':
        topic_form = TopicForm(request.POST, instance=topic)
        if topic_form.is_valid():
            topic_form.save()
            return redirect('part_details', course_id=part.course.id, part_id=part.id)
    else:
        topic_form = TopicForm(instance=topic, initial={'part_id': part.id})

    context = {
        'topic_form': topic_form,
        'part': part,
    }

    return render(request, 'update_topic.html', context)


def delete_topic(request, topic_id):
    topic = get_object_or_404(CourseTopic, id=topic_id)
    part = get_object_or_404(CoursePart, id=topic.part.id)
    course_id = part.course.id

    if request.method == 'POST':
        topic.delete()
        return redirect('part_details', course_id=course_id, part_id=part.id)

    return render(request, 'confirm_delete_topic.html', {'topic': topic})


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
    return render(request, 'documents/document_list.html', {'form': form, 'documents': documents})


def update_document(request, document_id):
    document = get_object_or_404(TopicDocument, id=document_id)

    if request.method == 'POST':
        form = TopicDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = TopicDocumentForm(instance=document)

    return render(request, 'documents/update_document.html', {'form': form, 'document': document})


def delete_document(request, document_id):
    document = get_object_or_404(TopicDocument, id=document_id)

    if request.method == 'POST':
        # delete file itself
        # if document.file:
        #     document.file.delete(save=False)
        # delete db row
        document.delete()
        return redirect('document_list')

    return render(request, 'documents/confirm_delete.html', {'document': document})

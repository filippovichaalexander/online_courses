from django.urls import path

from . import views

urlpatterns = [
    # path('', views.courses_list, name='courses_list'),
    path("courses_list/", views.courses_list, name="courses_list"),
    path("courses_list/<int:course_id>/", views.course_details, name="course_details"),
    path("courses_list/<int:course_id>/create_part/", views.create_course_part, name="create_course_part"),
    path("courses_list/<int:course_id>/course_parts/<int:part_id>", views.part_details, name="part_details"),
    path("document_list/", views.document_list, name="document_list"),
    path("update_course/<int:course_id>", views.update_course, name="update_course"),
    path("update_part/<int:part_id>", views.update_part, name="update_part"),
    path("update_topic/<int:topic_id>/", views.update_topic, name="update_topic"),
    path("confirm_delete_course/<int:course_id>", views.delete_course, name="confirm_delete_course"),
    path("confirm_delete_part/<int:part_id>", views.delete_part, name="delete_part"),
    path("Confirm_delete_topic/<int:topic_id>", views.delete_topic, name="delete_topic"),
    path("update_document/<int:document_id>", views.update_document, name="update_document"),
    path("delete_document/<int:document_id>", views.delete_document, name="delete_document"),
]

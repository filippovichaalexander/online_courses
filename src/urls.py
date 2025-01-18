"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from courses import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('courses_list/', views.courses_list, name='courses_list'),
                  path('courses_list/<int:course_id>/', views.course_details, name='course_details'),
                  path('courses_list/<int:course_id>/create_part/', views.create_course_part,
                       name='create_course_part'),
                  path('courses_list/<int:course_id>/course_parts/<int:part_id>', views.part_details,
                       name='part_details'),
                  path('document_list/', views.document_list, name='document_list'),
                  path('update_course/<int:course_id>', views.update_course, name='update_course'),
                  path('update_part/<int:part_id>', views.update_part, name='update_part'),
                  path('update_topic/<int:topic_id>/', views.update_topic, name='update_topic'),
                  path('confirm_delete_course/<int:course_id>', views.delete_course, name='confirm_delete_course'),
                  path('confirm_delete_part/<int:part_id>', views.delete_part, name='delete_part'),
                  path('Confirm_delete_topic/<int:topic_id>', views.delete_topic, name='delete_topic'),
                  path('delete_document/<int:document_id>', views.delete_document, name='delete_document'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

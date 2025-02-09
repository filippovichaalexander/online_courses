from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Course, CoursePart, CourseTopic


class CourseModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.course_data = {
            "title": "Python for Beginners",
            "description": "A comprehensive course for Python programming.",
            "created_by": self.user,
        }

    # 1 Проверка правильности создания экземпляра модели
    def test_course_creation(self):
        course = Course.objects.create(**self.course_data)

        self.assertEqual(course.title, "Python for Beginners")
        self.assertEqual(course.description, self.course_data["description"])
        self.assertEqual(course.created_by, self.course_data["created_by"])

    # 3. Проверка методов модели
    def test_soft_delete_and_restore(self):
        course = Course.objects.create(**self.course_data)
        course.delete()  # Используем мягкое удаление
        self.assertIsNotNone(course.deleted_at)  # Убедиться, что deleted_at установлен
        self.assertTrue(course.is_deleted)  # Проверить, что is_deleted работает корректно

        course.restore()  # Восстановление
        self.assertIsNone(course.deleted_at)  # Убедиться, что deleted_at снова None
        self.assertFalse(course.is_deleted)

    def test_hard_delete(self):
        course = Course.objects.create(**self.course_data)
        course.hard_delete()  # Полное удаление
        self.assertEqual(Course.all_objects.count(), 0)  # Убедиться, что запись удалена из базы


class CourseDetailViewTest(TestCase):
    def setUp(self):
        # Создаем пользователя и курс
        self.user = User.objects.create_user(username="testuser", password="password123")
        group = Group.objects.create(name="Instructors")
        self.instructor = User.objects.create_user(username="instructor", password="password123")
        self.instructor.groups.add(group)
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            created_by=self.instructor,
        )
        self.url = reverse("course_detail", kwargs={"pk": self.course.pk})  # URL для CourseDetailView
        self.client = Client()

    # 1. Проверка ответов на запросы
    def test_response_status(self):
        self.client.login(username="instructor", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Убедиться, что статус ответа 200

    def test_response_content(self):
        self.client.login(username="instructor", password="password123")
        response = self.client.get(self.url)
        self.assertContains(response, "Test Course")  # Убедиться, что содержимое содержит название курса
        self.assertContains(response, "Test Description")

    def test_response_headers_and_cookies(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertIn("Content-Type", response.headers)  # Проверка заголовков
        self.assertEqual(response.headers["Content-Type"], "text/html; charset=utf-8")
        self.assertNotIn("csrftoken", response.cookies)  # Проверяем cookies

    # 2. Тестирование перенаправлений
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Убедиться, что перенаправление на страницу логина
        self.assertIn(reverse("login"), response.url)  # URL должен содержать путь логина

    # 3. Проверка контекста шаблона
    def test_context_data(self):
        self.client.login(username="instructor", password="password123")
        # Создаем связанные данные для контекста
        course_part = CoursePart.objects.create(course=self.course, title="Part 1")
        CourseTopic.objects.create(part=course_part, title="Topic 1")
        response = self.client.get(self.url)
        self.assertIn("course_parts", response.context)  # Убедиться, что контекст содержит course_parts
        self.assertEqual(len(response.context["course_parts"]), 1)  # Проверяем количество частей курса
        self.assertEqual(response.context["course_parts"][0], course_part)  # Проверяем правильность данных

    # 4. Тестирование авторизации и доступа
    def test_access_denied_for_non_instructors(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)  # Убедиться, что доступ запрещен

    def test_access_allowed_for_instructor(self):
        self.client.login(username="instructor", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Убедиться, что доступ разрешен


class CoursePartModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.course = Course.objects.create(
            title="Python for Beginners",
            description="A comprehensive course for Python programming.",
            created_by=self.user,
        )
        self.part_data = {
            "course": self.course,
            "title": "Introduction to Python",
            "created_by": self.user,
        }

    def test_course_part_creation(self):
        part = CoursePart.objects.create(**self.part_data)
        self.assertEqual(part.title, "Introduction to Python")
        self.assertEqual(part.course, self.course)
        self.assertEqual(part.created_by, self.user)

    def test_soft_delete_and_restore(self):
        part = CoursePart.objects.create(**self.part_data)
        part.delete()  # Soft delete
        self.assertIsNotNone(part.deleted_at)
        self.assertTrue(part.is_deleted)

        part.restore()  # Restore
        self.assertIsNone(part.deleted_at)
        self.assertFalse(part.is_deleted)

    def test_hard_delete(self):
        part = CoursePart.objects.create(**self.part_data)
        part.hard_delete()  # Hard delete
        self.assertEqual(CoursePart.all_objects.count(), 0)


class PartDetailsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.course = Course.objects.create(
            title="Python for Beginners",
            description="A comprehensive course for Python programming.",
            created_by=self.user,
        )
        self.part = CoursePart.objects.create(
            course=self.course,
            title="Introduction to Python",
            created_by=self.user,
        )
        self.url = reverse("part_details", kwargs={"course_id": self.course.id, "part_id": self.part.id})
        self.client = Client()

    def test_response_status(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_response_content(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertContains(response, "Introduction to Python")

    def test_context_data(self):
        self.client.login(username="testuser", password="password123")
        topic = CourseTopic.objects.create(part=self.part, title="Variables in Python", created_by=self.user)
        response = self.client.get(self.url)
        self.assertIn("topics", response.context)
        self.assertEqual(len(response.context["topics"]), 1)
        self.assertEqual(response.context["topics"][0], topic)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)


class CreateCoursePartViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.course = Course.objects.create(
            title="Python for Beginners",
            description="A comprehensive course for Python programming.",
            created_by=self.user,
        )
        self.url = reverse("create_course_part", kwargs={"course_id": self.course.id})
        self.client = Client()

    def test_response_status(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_part_creation(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(self.url, {"title": "Introduction to Python", "course_id": self.course.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CoursePart.objects.count(), 1)
        self.assertEqual(CoursePart.objects.first().title, "Introduction to Python")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)


class UpdatePartViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.course = Course.objects.create(
            title="Python for Beginners",
            description="A comprehensive course for Python programming.",
            created_by=self.user,
        )
        self.part = CoursePart.objects.create(
            course=self.course,
            title="Introduction to Python",
            created_by=self.user,
        )
        self.url = reverse("update_part", kwargs={"part_id": self.part.id})
        self.client = Client()

    def test_response_status(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_part_update(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(self.url, {"title": "Advanced Python", "course_id": self.course.id})
        self.assertEqual(response.status_code, 302)
        self.part.refresh_from_db()
        self.assertEqual(self.part.title, "Advanced Python")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)


class DeletePartViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.course = Course.objects.create(
            title="Python for Beginners",
            description="A comprehensive course for Python programming.",
            created_by=self.user,
        )
        self.part = CoursePart.objects.create(
            course=self.course,
            title="Introduction to Python",
            created_by=self.user,
        )
        self.url = reverse("delete_part", kwargs={"part_id": self.part.id})
        self.client = Client()

    def test_response_status(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_part_deletion(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CoursePart.objects.count(), 0)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

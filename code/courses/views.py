import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView

from .forms import CompleteChapterForm
from .forms import StartCourseForm
from .models import Course
from lib.butter_cms_client import client

logger = logging.getLogger("root")


class PageTypeMixin(SingleObjectMixin):
    def get_object(self):
        slug = self.kwargs.get("slug")
        return client.pages.get(self.page_type, slug, {"levels": 3})


class SingleCourseMixin(SingleObjectMixin):
    def get_object(self):
        return self.get_queryset().get(butter_id=self.kwargs.get("butter_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = client.content_fields.get(["courses"], {"levels": 3})["data"][
            "courses"
        ]

        selected_course = next(
            (
                course
                for course in courses
                if course["meta"]["id"] == self.object.butter_id
            )
        )

        context["course"] = selected_course
        logger.info(selected_course)

        context["current_chapter"] = next(
            (
                chapter
                for chapter in selected_course["chapters"]
                if chapter["meta"]["id"] == self.object.current_chapter
            )
        )

        return context


class GetCourseCover(PageTypeMixin, DetailView):
    page_type = "course_cover"
    template_name = "courses/course_cover.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StartCourseForm()
        return context


class StartCourse(LoginRequiredMixin, PageTypeMixin, FormView):
    page_type = "course_cover"
    template_name = "courses/course_cover.html"
    form_class = StartCourseForm
    success_url = "/learn/"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)


class CourseCover(View):
    def get(self, request, *args, **kwargs):
        view = GetCourseCover.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = StartCourse.as_view()
        return view(request, *args, **kwargs)


class MyCourses(LoginRequiredMixin, TemplateView):
    template_name = "courses/my-courses.html"

    def get_context_data(self):
        context = super().get_context_data()
        courses = client.content_fields.get(["courses"])["data"]["courses"]
        user_courses_id = [
            user_course.butter_id
            for user_course in self.request.user.student.courses.all()
        ]

        user_courses = [
            course for course in courses if course["meta"]["id"] in user_courses_id
        ]
        context["user_courses"] = user_courses
        return context


class CourseDetail(LoginRequiredMixin, SingleCourseMixin, DetailView):
    model = Course
    template_name = "courses/chapter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CompleteChapterForm()

        return context


class CompleteChapter(LoginRequiredMixin, SingleCourseMixin, UpdateView):
    model = Course
    form_class = CompleteChapterForm
    template_name = "courses/chapter.html"

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        return super().form_valid(form)


class Course(View):
    def get(self, request, *args, **kwargs):
        view = CourseDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CompleteChapter.as_view()
        return view(request, *args, **kwargs)

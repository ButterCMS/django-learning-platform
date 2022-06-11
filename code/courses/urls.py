from django.urls import path

from . import views

urlpatterns = [
    path(
        "catalogue/<slug:slug>/",
        views.CourseCover.as_view(),
        name="catalogue_course_detail",
    ),
    path("learn/<int:butter_id>/", views.Course.as_view(), name="learn_course"),
    path("learn/", views.MyCourses.as_view(), name="learn_index"),
]

from django import forms

from .models import Course


class StartCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["student", "butter_id", "current_chapter"]


class CompleteChapterForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["current_chapter"]

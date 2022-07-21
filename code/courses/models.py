from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.constraints import UniqueConstraint

User = get_user_model()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)


class Course(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.PROTECT, related_name="courses"
    )
    butter_id = models.IntegerField()
    current_chapter = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(
                name="a_student_can_only_start_a_course_once",
                fields=["student", "butter_id"],
            )
        ]



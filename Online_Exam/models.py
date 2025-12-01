from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from Academics.models import ClassRoom, Section

class Exam(models.Model):
    title = models.CharField(max_length=200)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='exams')
    sections = models.ManyToManyField(Section, related_name='exams')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes")
    attempts_allowed = models.PositiveIntegerField(default=1)
    points_per_question = models.FloatField(default=1.0)
    show_answers_after_submission = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('SA', 'Short Answer'),
    )

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='MCQ')
    marks = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.exam.title} - {self.text[:50]}"


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

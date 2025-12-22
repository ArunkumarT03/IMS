from django.db import models
from Online_Exam.models import Exam, Question, Option
from student.models import Student

class StudentExamRecord(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('not_started_yet', 'Not Started Yet'),
        ('expired', 'Expired'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    select_answer = models.CharField(max_length=250, null=True, blank=True)
    correct_answer = models.CharField(max_length=250)
    is_correct = models.BooleanField(default=False)
    mark_obtained = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    total_marks = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started_yet'
    )

    def __str__(self):
        return f"{self.student}-{self.exam}"

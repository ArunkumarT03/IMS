from django.db import models

# Create your models here.
class Subject(models.Model):
    SUBJECT_TYPES = (
        ('theory', 'Theory'),
        ('practical', 'Practical'),
        ('lab', 'Lab'),
    )

    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=SUBJECT_TYPES)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"
    
class ClassRoom(models.Model):
    cls = models.CharField(max_length=20)
    sec = models.CharField(max_length=5)

    class Meta:
        unique_together = ('cls', 'sec')

    def __str__(self):
        return f"{self.cls}-{self.sec}"
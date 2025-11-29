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
    cls=models.CharField(max_length=255)
    
    def __str__(self):
        return self.cls
    
class Section(models.Model):
    cls=models.ForeignKey(ClassRoom,on_delete=models.CASCADE,related_name='sections')
    sec=models.CharField(max_length=255)
    
    class Meta:
        unique_together=('cls','sec')
        
    def __str__(self):
        return f'{self.cls}-{self.sec}'
    
class AssignSubject(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject= models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('instructor.Instructor', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('classroom', 'section', 'subject')

    def __str__(self):
        return f"{self.classroom.cls} - {self.section.sec} - {self.subject.subject_name}"
    
class AssignClassTeacher(models.Model):
    ROLE_CHOICES = (
        ('class_teacher', 'Class Teacher'),
        ('assistant_teacher', 'Assistant Teacher'),
        ('hod', 'HOD'),
    )

    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    teacher = models.ForeignKey('instructor.Instructor', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('classroom', 'section', 'teacher')

    def __str__(self):
        return f"{self.classroom.cls} - {self.section.sec} - {self.teacher.name} ({self.role})"

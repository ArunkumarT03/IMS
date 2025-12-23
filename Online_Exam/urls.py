from django.urls import path
from .views import *  


urlpatterns = [

  
    
    # GET → all exams  
    # POST → create exam
    path('exams/', ExamListCreateView.as_view(), name='exam-list-create'),

    # GET → exam by id  
    # PUT → update exam  
    # DELETE → delete exam
    path('exams/<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),
    path('questions/<int:exam_id>/', ExamQuestionsView.as_view()),


    
    # GET → all questions for exam  
    # POST → create question in exam
   path('exams/<int:student_id>/<int:classroom_id>/<int:section_id>/',ExamByStudentClassSectionView.as_view()),

      

    #GET - ALL QUESTIONS
    path('questions/',QuestionListView.as_view()), 
   
    # GET → single question  
    # PUT → update  
    # DELETE → delete
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
]

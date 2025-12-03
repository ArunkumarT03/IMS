from django.urls import path
from .views import ExamListCreateView,ExamDetailView,ExamQuestionListCreateView,QuestionDetailView,QuestionListView  


urlpatterns = [

  
    
    # GET → all exams  
    # POST → create exam
    path('exams/', ExamListCreateView.as_view(), name='exam-list-create'),

    # GET → exam by id  
    # PUT → update exam  
    # DELETE → delete exam
    path('exams/<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),


    
    # GET → all questions for exam  
    # POST → create question in exam
    path('exams/<int:exam_id>/questions/', ExamQuestionListCreateView.as_view(),  name='exam-question-list-create'),
      

    #GET - ALL QUESTIONS
    path('questions/',QuestionListView.as_view()), 
   
    # GET → single question  
    # PUT → update  
    # DELETE → delete
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
]

from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('quiz/', views.quiz_home, name='quiz_home'),  # ✅ Add a home route for quiz
    path('quiz/<int:pk>/', views.quiz_page, name='quiz_page'),  # ✅ Quiz page for a specific product
    path('quiz/start/<int:pk>/', views.quiz, name='quiz'),  # ✅ Start quiz (uses category filter)
    path('quiz/result/<int:pk>/', views.quiz_result, name='result'),  # ✅ Result page (fixes missing pk)
    path('add_question/', views.addQuestion, name='add_question'),  # ✅ Add essay question
]

  
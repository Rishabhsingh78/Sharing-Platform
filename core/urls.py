from django.urls import path
from .import views
urlpatterns = [
    path('register/',views.RegisterView, name= 'register'),
    path('login/',views.LoginView,name = 'login'),
    path('logout/',views.LogoutView, name= 'logout'),
    path('questions/',views.question_list_create,name = 'questions'),
    path('questions/<int:question_id>/answers/',views.answer_list_create,name = 'answers'),
    path('answers/',views.AnswerList, name= 'answer_list'),
    path('answer/<int:answer_id>/vote',views.vote_answer,name = 'vote_answer'),
]
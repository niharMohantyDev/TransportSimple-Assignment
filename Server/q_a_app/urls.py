from .views import *
from django.urls import path

urlpatterns = [
    path('users/register', register),
    path('users/login', login),
    path('users/logout',logout),
    path('api/post-question',postQuestions),
    path('api/post-answer',postAnswer),
    path('api/likes-dislikes',likesAndDislikes),
    path('api/get-all-questions', getEveryBodyQuestions),
    path('api/get-my-questions', getMyQuestions),
    path('api/get-answer', getAnswersForQuestion),
    path('api/archive-question', archiveQuestion),
    path('api/archive-answer', archiveAnswer)
]

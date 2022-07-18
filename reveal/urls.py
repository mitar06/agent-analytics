from django.urls import path, include
from .views import  SurveyList, SurveyRetrieve, QuestionList, ResponseAPIView, RevealAPIView

urlpatterns = [
    path('surveys/<str:id>/questions', QuestionList.as_view(), name='questions-list'),
    path('surveys/<str:id>', SurveyRetrieve.as_view(), name='survey-single'),
    path('surveys/',SurveyList.as_view(), name='survey-list' ),
    path('surveys/<str:id>/responses', ResponseAPIView.as_view(),name='response-list' ),
    path('surveys/<str:id>/reveal', RevealAPIView.as_view(), name='reveal')
]
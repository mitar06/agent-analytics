from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response as Resp
from .models import Answer, Question, Category,Survey, Response
from .serializers import AnswerSerializer, SurveySerializer, QuestionSerializer, ResponseSerializer

import pandas as pd

# Create your views here.
class SurveyList(generics.ListAPIView):
    serializer_class = SurveySerializer 
    queryset = Survey.objects.all()

class SurveyRetrieve(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = SurveySerializer

class QuestionList(generics.ListAPIView):
    serializer_class = QuestionSerializer 

    def get_queryset(self):
        return Question.objects.filter(survey__id=self.kwargs.get('id'))

class ResponseAPIView(APIView):
    
    def get(self, request,*args,**kwargs):
        user = User.objects.get(pk=1)
        survey_object = Survey.objects.prefetch_related('questions').get(pk=kwargs.get('id'))
        response = Response.objects.create(user=user, survey=survey_object)
        data  = AnswerSerializer(data=request.data['answers'], many=True,context={'response' : response})
        if data.is_valid():
            instances = data.save()
        return Resp(instances)


class RevealAPIView(APIView):

    def get(self, request, *args, **kwargs):
        bucket = Answer.objects.filter(response__survey__id=kwargs.get('id')).values('question__text', 'body','question_id')
        ser = AnswerSerializer(bucket, many=True)
        
        df = pd.DataFrame(ser.data)
        df.set_index(['question_id'])
        grouped = df.groupby('question_id')
        percentages = grouped['body'].value_counts(normalize=True) * 100
        percentages = percentages.to_frame()
        result = {}
        for index, row in percentages.iterrows():

            if index[0] in result:
                result[index[0]][index[1]] = row['body']
            else:
                result[index[0]] = {
                    index[1] : row['body']
                }

        return Resp(data=result)

        
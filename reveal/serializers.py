
from .models import Answer, Question, Category,Survey, Response
from rest_framework import serializers


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = [
            'id',
            'name',
            'description',
            'publish_date'
            ]

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Question
        fields = [
            'id',
            'text',
            'order',
            'type',
            'choices',
        ]

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'

        def create(self, validated_data):
           return Response.objects.create(**validated_data)

class AnswerSerializer(serializers.ModelSerializer):
    question__text = serializers.CharField(max_length=255)
    question_id = serializers.CharField(max_length=255)
    question = QuestionSerializer(many=True, read_only=True)
    response = ResponseSerializer(many=True, read_only=True)
    class Meta:
        model = Answer
        fields = '__all__'
    
    def create(self, validated_data):

        response = self.context['response']
        question = Question.objects.get(pk=validated_data['question_id'])
        answer = Answer.objects.create(question=question, response=response,body=validated_data['body'])
        return answer


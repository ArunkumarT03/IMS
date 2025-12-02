from rest_framework import serializers
from .models import Exam, Question, Option
from Academics.models import ClassRoom, Section

# Option Serializer
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']


# Question Serializer (nested options)
class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'marks', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if options_data:
            # Clear existing options and add new ones
            instance.options.all().delete()
            for option_data in options_data:
                Option.objects.create(question=instance, **option_data)
        return instance


# Exam Serializer (nested questions)
class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)
    sections = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all(), many=True)
    classroom = serializers.PrimaryKeyRelatedField(queryset=ClassRoom.objects.all())

    class Meta:
        model = Exam
        fields = [
            'id', 'title', 'classroom', 'sections',
            'start_time', 'end_time', 'time_limit', 'attempts_allowed',
            'points_per_question', 'show_answers_after_submission', 'questions'
        ]
        

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        sections_data = validated_data.pop('sections', [])
        exam = Exam.objects.create(**validated_data)
        exam.sections.set(sections_data)

        for question_data in questions_data:
            options_data = question_data.pop('options', [])
            question = Question.objects.create(exam=exam, **question_data)
            for option_data in options_data:
                Option.objects.create(question=question, **option_data)

        return exam

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', [])
        sections_data = validated_data.pop('sections', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.sections.set(sections_data)
        instance.save()

        if questions_data:
            instance.questions.all().delete()
            for question_data in questions_data:
                options_data = question_data.pop('options', [])
                question = Question.objects.create(exam=instance, **question_data)
                for option_data in options_data:
                    Option.objects.create(question=question, **option_data)
        return instance

from rest_framework import serializers
from .models import Exam, Question, Option
from Academics.models import ClassRoom, Section

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'marks', 'options', 'image']

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)
    classroom = serializers.SerializerMethodField()  # GET as string
    sections = serializers.SerializerMethodField()   # GET as list of strings

    classroom_name = serializers.CharField(write_only=True)       # POST/PUT
    section_names = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )

    class Meta:
        model = Exam
        fields = [
            'id', 'title', 'classroom', 'sections',
            'classroom_name', 'section_names',
            'start_time', 'end_time', 'time_limit', 'attempts_allowed',
            'points_per_question', 'show_answers_after_submission', 'questions'
        ]

    # GET methods
    def get_classroom(self, obj):
        return obj.classroom.cls  # replace 'cls' with your classroom field

    def get_sections(self, obj):
        section_id = self.context.get("section_id")

        if section_id:
            return list(
                obj.sections
                .filter(id=section_id)
                .values_list("sec", flat=True)
            )

        return [s.sec for s in obj.sections.all()]

    # POST / PUT
    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        classroom_name = validated_data.pop('classroom_name')
        section_names = list(set(validated_data.pop('section_names', [])))

    # Get classroom
        classroom = ClassRoom.objects.get(cls=classroom_name)
        validated_data['classroom'] = classroom

    # Create exam
        exam = Exam.objects.create(**validated_data)

    # Get sections only for this classroom
        sections = Section.objects.filter(cls=classroom, sec__in=section_names)
        exam.sections.set(sections)

    # Create questions
        for q_data in questions_data:
            options_data = q_data.pop('options', [])
            question = Question.objects.create(exam=exam, **q_data)
            for o_data in options_data:
                Option.objects.create(question=question, **o_data)

        return exam


    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', [])
        classroom_name = validated_data.pop('classroom_name', None)
        section_names = validated_data.pop('section_names', None)

        if classroom_name:
            instance.classroom = ClassRoom.objects.get(cls=classroom_name)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if section_names is not None:
            section_names = list(set(section_names))
            sections = Section.objects.filter( cls=instance.classroom,sec__in=section_names)
            instance.sections.set(sections)

        if questions_data:
            instance.questions.all().delete()
            for q_data in questions_data:
                options_data = q_data.pop('options', [])
                question = Question.objects.create(exam=instance, **q_data)
                for o_data in options_data:
                    Option.objects.create(question=question, **o_data)

        return instance
      
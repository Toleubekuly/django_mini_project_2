from rest_framework import serializers
from .models import Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'student', 'course', 'grade', 'date', 'teacher']
        extra_kwargs = {
            'teacher': {'read_only': True},
        }
